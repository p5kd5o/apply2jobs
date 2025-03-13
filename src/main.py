import logging
import os
import pathlib
import urllib
import urllib.parse

import mistralai
import pymupdf4llm
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
    logging.basicConfig()

    main_config = config.load_config_file(CONFIG_FILE)
    search_site_jobs_config = {
        site.host: site.jobs
        for site in main_config.search.sites
    }
    search_clients = _init_search_clients(main_config.search.sites)
    resume_md = pymupdf4llm.to_markdown(RESUME_PDF)

    webdriver_options = selenium.webdriver.FirefoxOptions()
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)
    for site, job_searches in search_site_jobs_config.items():
        try:
            search_func = sites.SEARCH_SUPPORTED[site]
            for job_search in job_searches:
                try:
                    for job in search_func(
                        search_clients[site], **job_search.to_dict()
                    ):
                        logging.debug(">>> Job:\n\n%s", job)
                        try:
                            hostname = urllib.parse.urlparse(
                                job.apply_url
                            ).hostname
                            submit_func = sites.SUBMIT_SUPPORTED[hostname]
                            logging.info(
                                "Applying to job: %s: %s: %s",
                                job.company_name, job.title, job.apply_url
                            )
                            if main_config.apply.confirm_before_submit:
                                input("<ENTER> to Continue...")
                            submit_func(
                                job,
                                resume_md,
                                RESUME_PDF,
                                COVER_LETTER_DIR,
                                webdriver,
                                mistral_client
                            )
                        except KeyError:
                            logging.warning(
                                "No support for site: %s",
                                hostname
                            )
                        except Exception as exc:
                            logging.warning("%s", exc)
                except Exception as exc:
                    logging.warning("%s", exc)
        except KeyError:
            logging.warning(
                "No support for site: %s",
                site
            )

    # webdriver.close()


if __name__ == "__main__":
    main()
