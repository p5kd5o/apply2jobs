import logging
import os
import pathlib
import urllib
import urllib.parse

import linkedin_api
import mistralai
import pymupdf4llm
import selenium.webdriver

import sites


logging.basicConfig()

RESUME_PDF = "/home/pat/Documents/Jobs/Resumes/Resume - Software Engineer - Patrick DeYoreo - 2025.pdf"
COVER_LETTER_DIR = pathlib.Path("/home/pat/Documents/Jobs/Cover_Letters")

MISTRAL_MODEL = "mistral-large-latest"
with open("api-keys/mistral-api-apply4jobs.key", encoding="utf-8") as istream:
    MISTRAL_API_KEY = istream.read().strip()

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

SEARCH_KWGS = {
    "www.linkedin.com": dict(
        keywords="software engineer",
        job_type="F",
        remote="2",
        location_name="United States",
        limit=5
    ),
}
SEARCH_CLIENTS = {
    "www.linkedin.com": linkedin_api.Linkedin(
        LINKEDIN_USERNAME, LINKEDIN_PASSWORD
    ),
}



def main():
    resume_md = pymupdf4llm.to_markdown(RESUME_PDF)

    webdriver_options = selenium.webdriver.FirefoxOptions()
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)
    for site, search_func in sites.SEARCH_SUPPORTED.items():
        try:
            for job in search_func(SEARCH_CLIENTS[site], **SEARCH_KWGS[site]):
                try:
                    hostname = urllib.parse.urlparse(job.apply_url).hostname
                    submit_func = sites.SUBMIT_SUPPORTED.get(
                        hostname.replace("-", "_")
                    )
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
                        submit_func(
                            job,
                            resume_md,
                            RESUME_PDF,
                            COVER_LETTER_DIR,
                            webdriver,
                            mistral_client
                        )
                except Exception:
                    pass
        except Exception:
            pass

    # webdriver.close()


if __name__ == "__main__":
    main()
