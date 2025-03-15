import logging
import pathlib
import time
from typing import Any, Callable

import bs4
import mistralai
import pymupdf4llm
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from models import Job, ApplyPersonalConfig
from sites.base import BaseSubmit
from utils import cover_letters

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class Submit(BaseSubmit):
    webdriver: WebDriver
    mistral_client: mistralai.Mistral
    pre_submit_hook: list[Callable[[], Any]]

    def __init__(
        self,
        webdriver: WebDriver,
        mistral_client: mistralai.Mistral,
        pre_submit_hook: list[Callable[[], Any]] = None
    ):
        self.webdriver = webdriver
        self.mistral_client = mistral_client
        if pre_submit_hook is None:
            self.pre_submit_hook = []
        else:
            self.pre_submit_hook = pre_submit_hook.copy()

    def main(
        self,
        job: Job,
        personal: ApplyPersonalConfig,
        resume_path: str | pathlib.Path,
        cover_letter_dir: str | pathlib.Path
    ) -> None:
        resume_path = pathlib.Path(resume_path)
        cover_letter_dir = pathlib.Path(cover_letter_dir)

        resume_md = pymupdf4llm.to_markdown(resume_path)

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
        cover_letters.save_cover_letter(cover_letter_md, cover_letter_path)

        for application_questions in application_form.find_all(
                "div",
                attrs={"class": "application--questions"},
                recursive=False
        ):
            for question in application_questions.children:
                question_div = question.div
                if question_div is None or "class" not in question_div.attrs:
                    continue
                attr_class = question_div.attrs["class"]
                if "text-input-wrapper" in attr_class:
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
                    match question_label.contents[0].casefold():
                        case "first name":
                            question_input_element.send_keys(
                                personal.first_name
                            )
                        case "last name":
                            question_input_element.send_keys(
                                personal.last_name
                            )
                        case "full name" | "name":
                            question_input_element.send_keys(
                                f"{personal.first_name} {personal.last_name}"
                            )
                        case "email" | "email address":
                            question_input_element.send_keys(
                                personal.contact.email_address
                            )
                        case "phone" | "phone number":
                            question_input_element.send_keys(
                                personal.contact.phone_number
                            )
                        case "linkedin" | "linkedin profile":
                            question_input_element.send_keys(
                                personal.social.linkedin
                            )
                        case "how did you hear about this job?":
                            question_input_element.send_keys(
                                job.source.shortname
                            )
                elif "select" in attr_class:
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
                    match question_label.contents[0].casefold():
                        case "location" | "city" | "location (city)":
                            question_input_element.send_keys(
                                personal.location.to_str(
                                    street_address=False, zip_code=False, country=False
                                )
                            )
                            time.sleep(0.33)
                            question_input_element.send_keys(Keys.RETURN)
                        case value if "authorized to work" in value:
                            question_input_element.send_keys(
                                "Yes" if personal.demographic.authorized_to_work
                                else "No"
                            )
                            time.sleep(0.33)
                            question_input_element.send_keys(Keys.RETURN)
                        case value if "sponsorship" in value:
                            question_input_element.send_keys(
                                "Yes" if personal.demographic.immigration_sponsorship
                                else "No"
                            )
                            time.sleep(0.33)
                            question_input_element.send_keys(Keys.RETURN)
                        case value if "agree" in value:
                            question_input_element.send_keys("I agree")
                            time.sleep(0.33)
                            question_input_element.send_keys(Keys.RETURN)
                elif "file-upload" in attr_class:
                    question_input = question_div.find("input")
                    question_label = question_div.find(
                        "div",
                        attrs={"class": "label"},
                        recursive=False
                    )
                    question_input_element = self.webdriver.find_element(
                        by=By.ID, value=question_input.attrs["id"]
                    )
                    match question_label.contents[0].casefold().replace(" ", ""):
                        case "resume" | "cv" | "resume/cv":
                            question_input_element.send_keys(
                                str(resume_path)
                            )
                        case "coverletter":
                            question_input_element.send_keys(
                                str(cover_letter_path)
                            )

        for demographic_section in application_form.find_all(
            "div",
            attrs={"id": "demographic-section"}
        ):
            for question_div in demographic_section.find_all(
                "div",
                attrs={"class": "select"},
                recursive=False
            ):
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
                match question_label.contents[0].casefold():
                    case value if "gender identity" in value:
                        question_input_element.send_keys(
                            personal.demographic.gender
                        )
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "transgender experience" in value:
                        question_input_element.send_keys(
                            "Yes" if personal.demographic.transgender
                            else "No"
                        )
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "sexual orientation" in value:
                        question_input_element.send_keys(
                            personal.demographic.sexual_orientation
                        )
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "disability" in value:
                        question_input_element.send_keys(
                            "Yes" if personal.demographic.disability
                            else "No"
                        )
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "veteran" in value:
                        question_input_element.send_keys(
                            "Yes" if personal.demographic.veteran
                            else "No"
                        )
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "ethnicities" in value:
                        for race in personal.demographic.races:
                            question_input_element.send_keys(race)
                            time.sleep(0.33)
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
