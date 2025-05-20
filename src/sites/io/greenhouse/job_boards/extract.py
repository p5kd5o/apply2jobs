from logging import getLogger
from urllib.parse import urljoin

import bs4
import requests

from models import Job, Form, Field
from utils.types import ResultWithErrors
from sites.base import _BaseExtract

LOGGER = getLogger(__name__)


# pylint: disable=too-few-public-methods
class Extract(_BaseExtract):
    def main(self, job: Job) -> Form:
        resp = requests.get(job.apply_url, timeout=10)
        soup = bs4.BeautifulSoup(resp.text, features="lxml")
        extract_form_result = self.__extract_form(job, soup)
        for error in extract_form_result.errors:
            LOGGER.warning("Error extracting field: %s", error)
        return extract_form_result.result

    @classmethod
    def __extract_form(
        cls, job: Job, soup: bs4.BeautifulSoup
    ) -> ResultWithErrors[Form]:
        extract_field_funcs = {
            "file-upload": cls.__extract_file_field,
            "text-input-wrapper": cls.__extract_text_field,
            "select": cls.__extract_select_field,
        }
        application_form = soup.find(
            "form", attrs={"id": "application-form"}
        )
        question_divs = application_form.find_all(
            "div", attrs={"class": list(extract_field_funcs.keys())}
        )
        fields = []
        errors = []
        for div in question_divs:
            try:
                match div.attrs["class"][0]:
                    case "file-upload":
                        fields.append(cls.__extract_file_field(div))
                    case "text-input-wrapper":
                        fields.append(cls.__extract_text_field(div))
                    case "select":
                        fields.append(cls.__extract_select_field(div))
                    case div_class:
                        errors.append(KeyError(
                            f"Unrecognized question div class``{div_class}''"
                        ))
            except Exception as exc:
                errors.append(exc)

        return ResultWithErrors(
            result=Form(
                fields=fields,
                method=application_form.attrs["method"],
                action=urljoin(
                    job.apply_url, application_form.attrs["action"]
                ),
                job_id=job._id
            ),
            errors=errors
        )

    @staticmethod
    def __extract_file_field(question_div: bs4.BeautifulSoup) -> Field:
        question_input = question_div.find("input")
        question_label = question_div.find(
            "div",
            attrs={"class": "label"},
            recursive=False
        )
        return Field(
            input_id=question_input.attrs.get("id"),
            input_name=question_input.attrs.get("name"),
            input_type=question_input.attrs.get("type"),
            input_value=question_input.attrs.get("value"),
            input_label=question_label.contents[0]
        )

    @staticmethod
    def __extract_text_field(question_div: bs4.BeautifulSoup) -> Field:
        question_input_wrapper = question_div.find(
            "div",
            attrs={"class": "input-wrapper"},
            recursive=False
        )
        question_input = question_input_wrapper.find("input")
        question_label = question_input_wrapper.label
        return Field(
            input_id=question_input.attrs.get("id"),
            input_name=question_input.attrs.get("name"),
            input_type=question_input.attrs.get("type"),
            input_value=question_input.attrs.get("value"),
            input_label=question_label.contents[0]
        )

    @staticmethod
    def __extract_select_field(question_div: bs4.BeautifulSoup) -> Field:
        question_select_container = question_div.find(
            "div",
            attrs={"class": "select__container"},
            recursive=False
        )
        question_input = question_select_container.find("input")
        question_label = question_select_container.label
        return Field(
            input_id=question_input.attrs.get("id"),
            input_name=question_input.attrs.get("name"),
            input_type=question_input.attrs.get("type"),
            input_value=question_input.attrs.get("value"),
            input_label=question_label.contents[0]
        )
