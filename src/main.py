import argparse
import logging
import os
import pathlib
import urllib
import urllib.parse

import mistralai
import selenium.webdriver
import selenium.common.exceptions

import services
import storage
import sites
import utils.config

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY",
    ""
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=lambda x: pathlib.Path(x).expanduser().absolute(),
        default=os.getenv(
            "APPLY2JOBS_CONFIG",
            "config.yaml"
        ),
        help="Application config file"
    )
    parser.add_argument(
        "--resume-pdf",
        type=lambda x: pathlib.Path(x).expanduser().absolute(),
        default=os.getenv(
            "APPLY2JOBS_RESUME_PDF",
            "resume.pdf"
        ),
        help="Resume PDF"
    )
    parser.add_argument(
        "--cover-letter-dir",
        type=lambda x: pathlib.Path(x).expanduser().absolute(),
        default=os.getenv(
            "APPLY2JOBS_COVER_LETTERS_DIR",
            "cover-letters/"
        ),
        help="Cover letter directory"
    )
    parser.add_argument(
        "--storage-backend",
        "-s",
        choices=storage.StorageBackendEnum,
        type=storage.StorageBackendEnum,
        default=os.getenv(
            "APPLY2JOBS_STORAGE_BACKEND",
            storage.StorageBackendEnum.FILESYSTEM.value
        ),
        help="Storage backend"
    )
    parser.add_argument(
        "--storage-uri",
        "-l",
        default=os.getenv(
            "APPLY2JOBS_STORAGE_URI",
            (pathlib.Path.cwd() / "apply2jobs.data").as_uri()
        ),
        help="Storage connection URI"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(level=getattr(logging, LOG_LEVEL))

    args = parse_args()

    main_config = utils.config.load_config_file(args.config)

    webdriver_options = selenium.webdriver.FirefoxOptions()

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)

    if main_config.apply.confirm_before_submit:
        pre_submit_hook = [lambda: input("<ENTER> to Continue...")]
    else:
        pre_submit_hook = None

    storage_backend = storage.STORAGE_BACKENDS[
        args.storage_backend
    ](args.storage_uri)

    ingest_service = services.IngestService(
        storage_backend,
        main_config.search.sites
    )
    ingest_results = ingest_service.ingest_all(
        main_config.search.sites
    )

    jobs_service = services.JobsService(
        storage_backend
    )
    jobs_results = jobs_service.get_all()

    for job in jobs_results:
        hostname = urllib.parse.urlparse(job.apply_url).hostname
        try:
            submit_supporter = sites.SUBMIT_SUPPORTED[hostname]
        except KeyError:
            logging.warning(
                "No ``submit'' support for site: %s",
                hostname
            )
        else:
            logging.info(
                "Submit: %s: %s: %s",
                job.company_name, job.title, job.apply_url
            )
            try:
                webdriver = selenium.webdriver.Firefox(
                    options=webdriver_options
                )
                submitter = submit_supporter(
                    webdriver, mistral_client,
                    pre_submit_hook=pre_submit_hook
                )
                results = submitter(
                    job,
                    main_config.apply.personal,
                    os.path.abspath(args.resume_pdf),
                    os.path.abspath(args.cover_letter_dir)
                )
                logging.info(
                    "Results:\n%s",
                    "\n".join(map(
                        lambda k, v: f"{k}: <{'>, <'.join(map(str, v))}>",
                        results.items()
                    )))
            except Exception as exc:
                logging.warning("%s", exc)
            finally:
                try:
                    webdriver.close()
                except selenium.common.exceptions.InvalidSessionIdException as exc:
                    logging.warning("%s", exc)


if __name__ == "__main__":
    main()
