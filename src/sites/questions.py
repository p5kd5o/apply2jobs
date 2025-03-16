import pathlib
import re

from selenium.webdriver.common.keys import Keys

from models import ApplyPersonalConfig, JobSource
from utils import matching
from . import patterns


def get_question_response(
    question: str,
    personal: ApplyPersonalConfig,
    job_source: JobSource,
    resume_path: str | pathlib.Path,
    cover_letter_path: str | pathlib.Path
) -> str:
    match matching.SearchRE(question, flags=re.IGNORECASE):
        case patterns.QUESTION_PATTERN_RESUME:
            return str(resume_path)
        case patterns.QUESTION_PATTERN_COVER_LETTER:
            return str(cover_letter_path)
        case patterns.QUESTION_PATTERN_FULLNAME:
            return personal.full_name
        case patterns.QUESTION_PATTERN_FIRSTNAME:
            return personal.first_name
        case patterns.QUESTION_PATTERN_LASTNAME:
            return personal.last_name
        case patterns.QUESTION_PATTERN_EMAIL:
            return personal.contact.email_address
        case patterns.QUESTION_PATTERN_PHONE:
            return personal.contact.phone_number
        case patterns.QUESTION_PATTERN_LINKEDIN:
            return personal.social.linkedin
        case patterns.QUESTION_PATTERN_GITHUB:
            return personal.social.github
        case patterns.QUESTION_PATTERN_WEBSITE:
            return personal.social.website
        case patterns.QUESTION_PATTERN_HOW_DID_YOU_HEAR:
            return job_source.shortname
        case patterns.QUESTION_PATTERN_MAILING_ADDRESS:
            return personal.location.to_str(country=False)
        case patterns.QUESTION_PATTERN_LOCATION_CITY:
            return personal.location.to_str(
                street_address=False, zip_code=False, country=False
            )
        case patterns.QUESTION_PATTERN_AUTHORIZED_TO_WORK:
            return (
                "Yes" if personal.demographic.authorized_to_work else "No"
            )
        case patterns.QUESTION_PATTERN_IMMIGRATION_SPONSORSHIP:
            return (
                "Yes" if personal.demographic.immigration_sponsorship else "No"
            )
        case patterns.QUESTION_PATTERN_AGREE:
            return "I agree"
        case patterns.QUESTION_PATTERN_GENDER_IDENTITY:
            return personal.demographic.gender
        case patterns.QUESTION_PATTERN_SEXUAL_ORIENTATION:
            return personal.demographic.sexual_orientation
        case patterns.QUESTION_PATTERN_SEX_GENDER:
            return personal.demographic.sex
        case patterns.QUESTION_PATTERN_TRANSGENDER:
            return personal.demographic.transgender_status
        case patterns.QUESTION_PATTERN_DISABILITY_STATUS:
            return personal.demographic.disability_status
        case patterns.QUESTION_PATTERN_VETERAN_STATUS:
            return personal.demographic.veteran_status
        case patterns.QUESTION_PATTERN_ETHNICITY:
            return personal.demographic.ethnicity
        case patterns.QUESTION_PATTERN_HISPANIC_LATINO:
            return personal.demographic.hispanic_status
        case patterns.QUESTION_PATTERN_RACES:
            return Keys.RETURN.join(personal.demographic.races)
        case patterns.QUESTION_PATTERN_UNITED_STATES:
            return "Yes" if patterns.QUESTION_PATTERN_UNITED_STATES.fullmatch(
                personal.location.country
            ) else "No"
    return ""
