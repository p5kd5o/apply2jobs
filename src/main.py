import json
import logging
import os
import pathlib
import urllib
import urllib.parse

import mistralai
import selenium.webdriver

import config
import models
import sites

CONFIG_FILE = os.getenv(
    "APPLY2JOBS_CONFIG",
    "config.yaml"
)

RESUME_PDF = os.getenv(
    "APPLY2JOBS_RESUME_PDF",
    "resume.pdf"
)
COVER_LETTER_DIR = pathlib.Path(os.getenv(
    "APPLY2JOBS_COVER_LETTERS_DIR",
    "cover_letters/"
))

MISTRAL_MODEL = "mistral-large-latest"
with open("api-keys/mistral-api-apply2jobs.key", encoding="utf-8") as istream:
    MISTRAL_API_KEY = istream.read().strip()


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
        level=getattr(logging, os.getenv("LOG_LEVEL", "WARNING"))
    )

    main_config = config.load_config_file(CONFIG_FILE)

    search_site_jobs_config = {
        site.host: site.jobs
        for site in main_config.search.sites
    }
    search_clients = _init_search_clients(main_config.search.sites)

    webdriver_options = selenium.webdriver.FirefoxOptions()
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    if main_config.apply.confirm_before_submit:
        pre_submit_hook = [lambda: input("<ENTER> to Continue...")]
    else:
        pre_submit_hook = None

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)
    for site, job_searches in search_site_jobs_config.items():
        try:
            search_func = sites.SEARCH_SUPPORTED[site](
                search_clients[site]
            ).main
        except KeyError:
            logging.warning(
                "No ``search'' support for site: %s",
                site
            )
        else:
            for job_search in job_searches:
                logging.info(
                    "Running search: %s: %s",
                    site,
                    json.dumps(job_search.to_dict())
                )
                try:
                    jobs = search_func(**job_search.to_dict())
                except Exception as exc:
                    logging.warning("%s", exc)
                else:
                    for job in jobs:
                        logging.debug(
                            ">>>>> Job:\n\n%s\n\n<<<<<",
                            job
                        )
                        hostname = urllib.parse.urlparse(
                            job.apply_url
                        ).hostname
                        try:
                            submit_func = sites.SUBMIT_SUPPORTED[hostname](
                                webdriver, mistral_client,
                                pre_submit_hook=pre_submit_hook
                            ).main
                        except KeyError:
                            logging.warning(
                                "No ``submit'' support for site: %s",
                                hostname
                            )
                        else:
                            logging.info(
                                "Applying to job: %s: %s: %s",
                                job.company_name, job.title, job.apply_url
                            )
                            try:
                                submit_func(
                                    job,
                                    main_config.apply.personal,
                                    RESUME_PDF,
                                    COVER_LETTER_DIR
                                )
                            except Exception as exc:
                                logging.warning("%s", exc)

    # webdriver.close()


if __name__ == "__main__":
    main()
