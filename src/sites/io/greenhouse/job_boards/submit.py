import logging
import pathlib
import time
from typing import Any, Callable, Iterable

import bs4
import mistralai
import pymupdf4llm
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from models import ApplyPersonalConfig, Job
from sites.base import _BaseSubmit
from sites.questions import get_question_response
from utils import cover_letters, pdf

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class Submit(_BaseSubmit):
    webdriver: WebDriver
    mistral_client: mistralai.Mistral
    pre_submit_hook: list[Callable[[], Any]]

    def __init__(
        self,
        webdriver: WebDriver,
        mistral_client: mistralai.Mistral,
        pre_submit_hook: Iterable[Callable[[], Any]] = None
    ):
        self.webdriver = webdriver
        self.mistral_client = mistral_client
        if pre_submit_hook is None:
            self.pre_submit_hook = []
        else:
            self.pre_submit_hook = list(pre_submit_hook)

    def main(
        self,
        job: Job,
        personal: ApplyPersonalConfig,
        resume_path: str | pathlib.Path,
        cover_letter_dir: str | pathlib.Path
    ) -> None:
        resume_path = pathlib.Path(resume_path)
        cover_letter_dir = pathlib.Path(cover_letter_dir)

        LOGGER.info(
            "Converting resume to Markdown: %s",
            resume_path
        )
        resume_md = pymupdf4llm.to_markdown(
            resume_path, show_progress=False
        )

        resp = requests.get(job.apply_url, timeout=10)
        soup = bs4.BeautifulSoup(resp.text, features="lxml")
        application_form = soup.find("form", attrs={"id": "application-form"})

        self.webdriver.get(job.apply_url)

        cover_letter_path = (
            cover_letter_dir /
            f"{job.company_name.replace(".", "")} - {job.title}.pdf"
        )
        cover_letter_md = cover_letters.generate_cover_letter(
            self.mistral_client, job.description, resume_md
        )
        pdf.md_to_pdf(cover_letter_md, cover_letter_path)

        for question_div in application_form.find_all(
            "div",
            attrs={
                "class": [
                    "file-upload",
                    "text-input-wrapper",
                    "select",
                ]
            }
        ):
            if "file-upload" in question_div.attrs["class"]:
                question_input = question_div.find("input")
                question_label = question_div.find(
                    "div",
                    attrs={"class": "label"},
                    recursive=False
                )
                question_input_element = self.webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                question_input_element.send_keys(
                    get_question_response(
                        question=question_label.contents[0],
                        personal=personal,
                        job_source=job.source,
                        resume_path=resume_path,
                        cover_letter_path=cover_letter_path
                    )
                )
            if "text-input-wrapper" in question_div.attrs["class"]:
                question_input_wrapper = question_div.find(
                    "div",
                    attrs={"class": "input-wrapper"},
                    recursive=False
                )
                question_input = question_input_wrapper.find("input")
                question_label = question_input_wrapper.label
                question_input_element = self.webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                question_input_element.send_keys(
                    get_question_response(
                        question=question_label.contents[0],
                        personal=personal,
                        job_source=job.source,
                        resume_path=resume_path,
                        cover_letter_path=cover_letter_path
                    )
                )
            if "select" in question_div.attrs["class"]:
                question_select_container = question_div.find(
                    "div",
                    attrs={"class": "select__container"},
                    recursive=False
                )
                question_input = question_select_container.find("input")
                question_label = question_select_container.label
                question_input_element = self.webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                for keystroke in get_question_response(
                    question=question_label.contents[0],
                    personal=personal,
                    job_source=job.source,
                    resume_path=resume_path,
                    cover_letter_path=cover_letter_path
                ):
                    question_input_element.send_keys(keystroke)
                    time.sleep(0.025)
                time.sleep(0.475)
                question_input_element.send_keys(Keys.RETURN)

        try:
            gdpr_data_checkbox_input_element = self.webdriver.find_element(
                by=By.ID, value="gdpr_demographic_data_consent_given_1"
            )
        except Exception:
            pass
        else:
            gdpr_data_checkbox_input_element.click()

        submit_button = self.webdriver.find_element(
            By.XPATH, '//button[text()="Submit application"]'
        )

        for func in self.pre_submit_hook:
            func()

        submit_button.click()
        time.sleep(1)
