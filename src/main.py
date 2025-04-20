import argparse
import logging
import os
import pathlib
import urllib.parse

import mistralai
import selenium.webdriver

import services
import sites
import storage
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
        type=lambda x: pathlib.Path(x).expanduser(),
        default=os.getenv(
            "APPLY2JOBS_CONFIG",
            "config.yaml"
        ),
        help="Config file"
    )
    parser.add_argument(
        "--resume-pdf",
        type=lambda x: pathlib.Path(x).expanduser(),
        default=os.getenv(
            "APPLY2JOBS_RESUME_PDF",
            "resume.pdf"
        ),
        help="Resume PDF"
    )
    parser.add_argument(
        "--cover-letter-dir",
        type=lambda x: pathlib.Path(x).expanduser(),
        default=os.getenv(
            "APPLY2JOBS_COVER_LETTERS_DIR",
            "coverletters/"
        ),
        help="Coverletter directory"
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

    mistral_client = mistralai.Mistral(api_key=MISTRAL_API_KEY)

    if main_config.submit.confirm_before_submit:
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
        try:
            hostname = urllib.parse.urlparse(job.apply_url).hostname
        except Exception as exc:
            logging.warning("%s", exc)
            continue

        try:
            submitter_type: type[sites._BaseSubmit] = (
                sites.SUBMIT_SUPPORTED[hostname]
            )
        except KeyError:
            logging.warning(
                "no ``submit'' support for site: %s",
                hostname
            )
            continue

        logging.info(
            "submit: %s: %s: %s",
            job.company_name, job.title, job.apply_url
        )
        try:
            webdriver_options = selenium.webdriver.FirefoxOptions()
            webdriver = selenium.webdriver.Firefox(
                options=webdriver_options
            )
            submitter = submitter_type(
                webdriver,
                mistral_client,
                pre_submit_hook=pre_submit_hook
            )
            submit_results = submitter.main(
                job,
                main_config.submit.personal,
                os.path.abspath(args.resume_pdf),
                os.path.abspath(args.cover_letter_dir)
            )
            for xpath, errors in submit_results.items():
                for err in filter(lambda e: e is not None, errors):
                    logging.warning(
                        "%s: %s: %s",
                        job.apply_url, xpath, err
                    )
        except Exception as exc:
            logging.warning("%s", exc)
        finally:
            try:
                webdriver.close()
            except Exception as exc:
                logging.warning("%s", exc)


if __name__ == "__main__":
    main()
