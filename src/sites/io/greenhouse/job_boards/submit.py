import dataclasses
import logging
import pathlib
import time
from typing import Callable, Self

import bs4
import pymupdf4llm
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from models import ApplyPersonalConfig, Job
from sites.base import _BaseSubmit
from sites.questions import get_question_response
from utils import cover_letters, pdf, xpath

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
@dataclasses.dataclass
class FormResponseInfo:
    job: Job
    personal: ApplyPersonalConfig
    resume_path: str | pathlib.Path
    cover_letter_path: str | pathlib.Path


# pylint: disable=too-few-public-methods
class Submit(_BaseSubmit):
    FillFormFuncType = Callable[
        [Self, FormResponseInfo, bs4.BeautifulSoup],
        Exception | None
    ]

    def main(
        self,
        job: Job,
        personal: ApplyPersonalConfig,
        resume_path: str | pathlib.Path,
        cover_letter_dir: str | pathlib.Path
    ) -> dict[str, list[Exception | None]]:
        resume_path = pathlib.Path(resume_path)
        cover_letter_dir = pathlib.Path(cover_letter_dir)

        LOGGER.info(
            "Convert resume to Markdown: %s",
            resume_path
        )
        resume_md = pymupdf4llm.to_markdown(
            resume_path, show_progress=False
        )

        resp = requests.get(job.apply_url, timeout=10)
        soup = bs4.BeautifulSoup(resp.text, features="lxml")

        cover_letter_path = (
            cover_letter_dir /
            f"{job.company_name.replace(".", "")} - {job.title}.pdf"
        )
        cover_letter_md = cover_letters.generate_cover_letter(
            self.mistral_client, job.description, resume_md
        )
        pdf.md_to_pdf(cover_letter_md, cover_letter_path)

        self.webdriver.get(job.apply_url)

        fill_form_funcs = {
            "file-upload": self.__fill_file_upload,
            "text-input-wrapper": self.__fill_text_input,
            "select": self.__fill_select,
        }
        fill_form_results = self.__fill_form(
            FormResponseInfo(job, personal, resume_path, cover_letter_path),
            soup,
            fill_form_funcs
        )

        submit_button = self.webdriver.find_element(
            By.XPATH, '//button[text()="Submit application"]'
        )
        for func in self.pre_submit_hook:
            func()
        submit_button.click()
        time.sleep(5)
        return fill_form_results

    def __fill_form(
        self,
        form_response_info: FormResponseInfo,
        soup: bs4.BeautifulSoup,
        fill_form_funcs: dict[str, FillFormFuncType]
    ) -> dict[str, list[Exception | None]]:
        application_form = soup.find(
            "form", attrs={"id": "application-form"}
        )
        question_divs = application_form.find_all(
            "div", attrs={"class": list(fill_form_funcs.keys())}
        )
        fill_form_results = {
            xpath.get_node_xpath(question_div):
            self.__fill_form_div(
                form_response_info, question_div, fill_form_funcs
            )
            for question_div in question_divs
        }
        try:
            gdpr_data_checkbox_input_element = self.webdriver.find_element(
                by=By.ID, value="gdpr_demographic_data_consent_given_1"
            )
        except Exception:
            pass
        else:
            gdpr_data_checkbox_input_element.click()

        return fill_form_results

    def __fill_form_div(
        self,
        form_response_info: FormResponseInfo,
        question_div: bs4.BeautifulSoup,
        fill_form_funcs: dict[str, FillFormFuncType]
    ) -> list[Exception | None]:
        return [
            fill_form_funcs[class_attr](form_response_info, question_div)
            if class_attr in fill_form_funcs
            else KeyError(f"Unrecognized question div class``{class_attr}''")
            for class_attr in question_div.attrs["class"]
        ]

    def __fill_file_upload(
        self,
        form_response_info: FormResponseInfo,
        question_div: bs4.BeautifulSoup
    ) -> Exception | None:
        try:
            question_input = question_div.find("input")
            question_label = question_div.find(
                "div",
                attrs={"class": "label"},
                recursive=False
            )
            question_input_element = self.webdriver.find_element(
                by=By.ID, value=question_input.attrs["id"]
            )
            question_response = get_question_response(
                question=question_label.contents[0],
                personal=form_response_info.personal,
                job_source=form_response_info.job.source,
                resume_path=form_response_info.resume_path,
                cover_letter_path=form_response_info.cover_letter_path
            )
            question_input_element.send_keys(question_response)
        except Exception as exc:
            return exc
        return None

    def __fill_text_input(
        self,
        form_response_info: FormResponseInfo,
        question_div: bs4.BeautifulSoup
    ) -> Exception | None:
        try:
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
            question_response = get_question_response(
                question=question_label.contents[0],
                personal=form_response_info.personal,
                job_source=form_response_info.job.source,
                resume_path=form_response_info.resume_path,
                cover_letter_path=form_response_info.cover_letter_path
            )
            question_input_element.send_keys(question_response)
        except Exception as exc:
            return exc
        return None

    def __fill_select(
        self,
        form_response_info: FormResponseInfo,
        question_div: bs4.BeautifulSoup
    ) -> Exception | None:
        try:
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
            question_response = get_question_response(
                question=question_label.contents[0],
                personal=form_response_info.personal,
                job_source=form_response_info.job.source,
                resume_path=form_response_info.resume_path,
                cover_letter_path=form_response_info.cover_letter_path
            )
            for keystroke in question_response:
                question_input_element.send_keys(keystroke)
                time.sleep(0.025)
            time.sleep(0.475)
            question_input_element.send_keys(Keys.RETURN)
        except Exception as exc:
            return exc
        return None
