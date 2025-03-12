import logging
import os
import pathlib
import urllib
import urllib.parse

import linkedin_api
import mistralai
import pymupdf4llm
import selenium.webdriver

import config
import models
import models.search_config
import models.search_element_auth_credential_config
import sites

CONFIG_FILE = os.getenv(
    "APPLY2JOBS_CONFIG",
    "config.yaml"
)

RESUME_PDF = os.getenv(
    "APPLY2JOBS_RESUME_PDF",
    "/home/pat/Documents/Jobs/Resumes/Resume - Software Engineer - Patrick DeYoreo - 2025.pdf"
)
COVER_LETTER_DIR = pathlib.Path(os.getenv(
    "APPLY2JOBS_COVER_LETTERS_PATH",
    "/home/pat/Documents/Jobs/Cover_Letters"
))

MISTRAL_MODEL = "mistral-large-latest"
with open("api-keys/mistral-api-apply2jobs.key", encoding="utf-8") as istream:
    MISTRAL_API_KEY = istream.read().strip()

SEARCH_SITE_CLIENT_TYPES = {
    "www.linkedin.com": linkedin_api.Linkedin
}


def main():
    logging.basicConfig()

    main_config = config.load_config_file(CONFIG_FILE)
    search_site_jobs_config = {
        site.host: site.jobs
        for site in main_config.search.sites
    }
    search_clients = {}
    for site in main_config.search.sites:
        search_client_kwgs = {}
        for name, credential in site.auth.credentials:
            print(credential.value_type)
            if (credential.value_type ==
                models.search_element_auth_credential_config
                .SearchElementCredentialValueType
                .PLAINTEXT
            ):
                search_client_kwgs[name] = credential.value
            if (credential.value_type ==
                models.search_element_auth_credential_config
                .SearchElementCredentialValueType
                .ENV
            ):
                search_client_kwgs[name] = os.getenv(credential.value)
        print(search_client_kwgs)
        search_clients[site.host] = SEARCH_SITE_CLIENT_TYPES[site.host](
            **search_client_kwgs
        )
    resume_md = pymupdf4llm.to_markdown(RESUME_PDF)

    webdriver_options = selenium.webdriver.FirefoxOptions()
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)
    for site, searches in search_site_jobs_config.items():
        try:
            search_func = sites.SEARCH_SUPPORTED[site]
            for job_search in searches:
                try:
                    search_kwgs = job_search.to_dict()
                    for job in search_func(search_clients[site], **search_kwgs):
                        logging.debug(">>> Job:\n\n%s", job)
                        try:
                            hostname = urllib.parse.urlparse(job.apply_url).hostname
                            submit_func = sites.SUBMIT_SUPPORTED.get(hostname)
                            if submit_func is None:
                                logging.warning(
                                    "No support for site: %s",
                                    hostname
                                )
                            else:
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
                        except Exception as exc:
                            logging.warning("%s", exc)
                except Exception as exc:
                    logging.warning("%s", exc)
        except KeyError:
            logging.warning(
                "Site not supported: %s",
                site
            )

    # webdriver.close()


if __name__ == "__main__":
    main()
