import argparse
import logging
import logging.handlers
import os
import pathlib
import signal
import sys
import typing
import urllib.parse

import mistralai
import selenium.webdriver

import services
import sites
import storage
import utils.config
import utils.logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
LOG_FMT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"

MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY",
    ""
)


def sigint_handler(_, __):
    print()
    logging.info("received SIGINT - Exiting...")
    sys.exit(128 + signal.SIGINT)


def configure_logging(
    level: int | str | None = "INFO",
    fmt: str | None = None,
    datefmt: str | None = None,
    style: str = "%",
    *,
    defaults: typing.Mapping[str, typing.Any] | None = None
) -> None:
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    if handler.stream.isatty():
        formatter = utils.logging.ColorFormatter(
            fmt, datefmt, style, defaults=defaults
        )
    else:
        formatter = logging.Formatter(
            fmt, datefmt, style, defaults=defaults
        )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(level)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=lambda x: pathlib.Path(x).expanduser(),
        default=os.getenv(
            "APPLY2JOBS_CONFIG",
            "config.yaml"
        ),
        help="Config file"
    )
    parser.add_argument(
        "-s",
        "--storage-backend",
        choices=storage.StorageBackendEnum,
        type=storage.StorageBackendEnum,
        default=os.getenv(
            "APPLY2JOBS_STORAGE_BACKEND",
            storage.StorageBackendEnum.FILESYSTEM.value
        ),
        help="Storage backend"
    )
    parser.add_argument(
        "-l",
        "--storage-uri",
        default=os.getenv(
            "APPLY2JOBS_STORAGE_URI",
            (pathlib.Path.cwd() / "apply2jobs.data").as_uri()
        ),
        help="Storage connection URI"
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
    return parser.parse_args()


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    configure_logging(level=LOG_LEVEL, fmt=LOG_FMT)

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
        *main_config.search.sites
    )
    ingest_ids = ingest_service.ingest_many(
        *main_config.search.sites
    )
    logging.debug("ingest IDs: %s", ingest_ids)

    jobs_service = services.JobsService(
        storage_backend
    )
    jobs = jobs_service.find_jobs()

    forms_service = services.FormsService(
        storage_backend
    )
    form_ids = forms_service.extract_many(*jobs)
    logging.debug("form IDs: %s", form_ids)

    for job in jobs:
        try:
            hostname = urllib.parse.urlparse(job.apply_url).hostname
        except Exception as exc:
            logging.warning("%s", exc)
            continue

        try:
            submitter_type = sites.SUBMIT_SUPPORTED[hostname]
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
