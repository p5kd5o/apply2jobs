import logging
import os
import pathlib
import urllib
import urllib.parse

import mistralai
import selenium.webdriver
import selenium.webdriver.remote.webdriver

import models
import sites
import utils.config

CONFIG_FILE = pathlib.Path(os.getenv(
    "APPLY2JOBS_CONFIG",
    "config.yaml"
)).absolute()

RESUME_PDF = pathlib.Path(os.getenv(
    "APPLY2JOBS_RESUME_PDF",
    "resume.pdf"
)).absolute()

COVER_LETTER_DIR = pathlib.Path(os.getenv(
    "APPLY2JOBS_COVER_LETTERS_DIR",
    "cover-letters/"
)).absolute()

MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY",
    ""
)


def _init_search_clients(
    search_sites: list[models.SearchElementConfig]
) -> dict[str, object]:
    search_clients = {}
    for site in search_sites:
        search_client_kwgs = {}
        for name, credential in site.auth.credentials:
            if (
                credential.value_type ==
                models.SearchElementAuthCredentialValueType.PLAINTEXT
            ):
                search_client_kwgs[name] = credential.value
            if (
                credential.value_type ==
                models.SearchElementAuthCredentialValueType.ENV
            ):
                search_client_kwgs[name] = os.getenv(credential.value)
        search_clients[site.host] = sites.SITE_CLIENT_TYPE[site.host](
            **search_client_kwgs
        )
    return search_clients


def main():
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "WARNING").upper())
    )

    main_config = utils.config.load_config_file(CONFIG_FILE)

    site_search_config = {
        site.host: site.jobs
        for site in main_config.search.sites
    }
    site_search_clients = _init_search_clients(main_config.search.sites)

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)

    webdriver_options = selenium.webdriver.FirefoxOptions()
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    if main_config.apply.confirm_before_submit:
        pre_submit_hook = [lambda: input("<ENTER> to Continue...")]
    else:
        pre_submit_hook = None

    for site, job_searches in site_search_config.items():
        try:
            search_func = sites.SEARCH_SUPPORTED[site](
                site_search_clients[site]
            )
        except KeyError:
            logging.warning(
                "No ``search'' support for site: %s",
                site
            )
            continue

        for job_search in job_searches:
            logging.info(
                "Search: %s: %s",
                site,
                job_search.model_dump_json()
            )
            try:
                jobs = search_func(**job_search.model_dump())
            except Exception as exc:
                logging.warning("%s", exc)
                continue

            for job in jobs:
                hostname = urllib.parse.urlparse(
                    job.apply_url
                ).hostname
                try:
                    submit_func = sites.SUBMIT_SUPPORTED[hostname](
                        webdriver,
                        mistral_client,
                        pre_submit_hook=pre_submit_hook
                    )
                except KeyError:
                    logging.warning(
                        "No ``submit'' support for site: %s",
                        hostname
                    )
                    continue

                logging.info(
                    "Submit: %s: %s: %s",
                    job.company_name, job.title, job.apply_url
                )
                try:
                    submit_func(
                        job,
                        main_config.apply.personal,
                        os.path.abspath(RESUME_PDF),
                        os.path.abspath(COVER_LETTER_DIR)
                    )
                except Exception as exc:
                    logging.warning("%s", exc)
                    continue

    # webdriver.close()


if __name__ == "__main__":
    main()
