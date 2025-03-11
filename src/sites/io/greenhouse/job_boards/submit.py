import logging
import time

import bs4
import mistralai
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from models import Job
from utils import cover_letters
from . import SITE, SITE_SHORTNAME

LOGGER = logging.getLogger(__name__)


def run(
        job: Job,
        resume_md: str,
        resume_path: str,
        cover_letter_dir: str,
        webdriver: WebDriver,
        mistral_client: mistralai.Mistral
) -> None:
    resp = requests.get(job.apply_url, timeout=10)
    soup = bs4.BeautifulSoup(resp.text)
    application_form = soup.find("form", attrs={"id": "application-form"})

    webdriver.get(job.apply_url)

    cover_letter_path = str(
        cover_letter_dir / f"{job.company_name.replace(".", "")} - {job.title}.pdf"
    )
    cover_letter_md = cover_letters.generate_cover_letter(
        mistral_client, job.description, resume_md
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
                question_input_element = webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                match question_label.contents[0].casefold():
                    case "first name":
                        question_input_element.send_keys("Patrick")
                    case "last name":
                        question_input_element.send_keys("DeYoreo")
                    case "full name" | "name":
                        question_input_element.send_keys("Patrick DeYoreo")
                    case "email" | "email address":
                        question_input_element.send_keys("pdeyoreo@gmail.com")
                    case "phone" | "phone number":
                        question_input_element.send_keys("925-487-6155")
                    case "linkedin"|"linkedin profile":
                        question_input_element.send_keys("https://linkedin.com/in/patrickdeyoreo")
                    case "how did you hear about this job?":
                        question_input_element.send_keys("LinkedIn")
            elif "select" in attr_class:
                question_select_container = question_div.find(
                    "div",
                    attrs={"class": "select__container"},
                    recursive=False
                )
                question_input = question_select_container.find("input")
                question_label = question_select_container.label
                question_input_element = webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                match question_label.contents[0].casefold():
                    case "location" | "city" | "location (city)":
                        question_input_element.send_keys("Ashland, Oregon, United States")
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "authorized to work" in value:
                        question_input_element.send_keys("Yes")
                        time.sleep(0.33)
                        question_input_element.send_keys(Keys.RETURN)
                    case value if "sponsorship" in value:
                        question_input_element.send_keys("No")
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
                question_input_element = webdriver.find_element(
                    by=By.ID, value=question_input.attrs["id"]
                )
                match question_label.contents[0].casefold().replace(" ", ""):
                    case "resume" | "cv" | "resume/cv":
                        question_input_element.send_keys(resume_path)
                    case "coverletter":
                        question_input_element.send_keys(cover_letter_path)

    for question_div in application_form.find(
            "div",
            attrs={"id": "demographic-section"}
    ).find_all(
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
        question_input_element = webdriver.find_element(
            by=By.ID, value=question_input.attrs["id"]
        )
        match question_label.contents[0].casefold():
            case value if "gender identity" in value:
                question_input_element.send_keys("Non-binary")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)
            case value if "transgender experience" in value:
                question_input_element.send_keys("No")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)
            case value if "sexual orientation" in value:
                question_input_element.send_keys("Heterosexual")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)
            case value if "disability" in value:
                question_input_element.send_keys("I don't wish to answer")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)
            case value if "veteran" in value:
                question_input_element.send_keys("No")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)
            case value if "ethnicities" in value:
                question_input_element.send_keys("White")
                time.sleep(0.33)
                question_input_element.send_keys(Keys.RETURN)

    gdpr_demographic_data_checkbox_input_element = webdriver.find_element(
        by=By.ID, value="gdpr_demographic_data_consent_given_1"
    )
    if gdpr_demographic_data_checkbox_input_element is not None:
        gdpr_demographic_data_checkbox_input_element.click()

    submit_button = webdriver.find_element(
        By.XPATH, '//button[text()="Submit application"]'
    )
    submit_button.click()

    time.sleep(1)
