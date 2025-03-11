import logging
import os
import pathlib
import importlib
import logging
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
# with open("api-keys/linkedin-apply4jobs-oauth-token", encoding="utf-8") as istream:
#     LINKEDIN_OAUTH_TOKEN = istream.read().strip()


def main():
    resume_md = pymupdf4llm.to_markdown(RESUME_PDF)

    webdriver_options = selenium.webdriver.FirefoxOptions() 
    # webdriver_options.add_argument("-headless")
    webdriver = selenium.webdriver.Firefox(options=webdriver_options)

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)
    linkedin_client = linkedin_api.Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    job_results = linkedin_client.search_jobs(keywords="software engineer", job_type="F", remote="2", location_name="United States", limit=5)
    for job_result in job_results:
        job = linkedin_client.get_job(job_result["entityUrn"].split(':')[-1])
        job_title = job["title"]
        job_company_name = job["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]
        job_description = job["description"]["text"]
        match job["applyMethod"]:
            case {"com.linkedin.voyager.jobs.ComplexOnsiteApply": {
                    "companyApplyUrl": job_apply_url
            }}:
                pass
            case {"com.linkedin.voyager.jobs.OffsiteApply": {
                    "companyApplyUrl": job_apply_url
            }}:
                pass
            case _:
                logging.warning(
                    "No company apply URL: %s: %s",
                    job_company_name, job_title
                )
                continue
        try:
            hostname = urllib.parse.urlparse(job_apply_url).hostname
            hostname_rev = ".".join(hostname.split(".")[::-1])
            apply_module = importlib.import_module(
                f".{hostname_rev.replace('-', '_')}.apply",
                package=sites.__package__
            )
        except ModuleNotFoundError:
            logging.warning(
                "No support for site: %s",
                hostname
            )
            continue

        logging.info(
            "Applying to job: %s: %s: %s",
            job_company_name, job_title, job_apply_url
        )
        getattr(apply_module, "run")(
            job_company_name,
            job_title,
            job_description,
            job_apply_url,
            resume_md,
            RESUME_PDF,
            COVER_LETTER_DIR,
            webdriver,
            mistral_client
        )
            
    webdriver.close()


if __name__ == "__main__":
    main()
