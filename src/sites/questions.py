import pathlib
import re

from selenium.webdriver.common.keys import Keys

from models import ApplyPersonalConfig, JobSource

QUESTION_PATTERNS = {
    "firstname": re.compile(
        r"\bfirst\s?name\b",
        flags=re.IGNORECASE
    ),
    "lastname": re.compile(
        r"\blast\s?name\b",
        flags=re.IGNORECASE
    ),
    "fullname": re.compile(
        r"\bfull\s?name\b",
        flags=re.IGNORECASE
    ),
    "email": re.compile(
        r"\be-?mail\b",
        flags=re.IGNORECASE
    ),
    "phone": re.compile(
        r"\bphone\b",
        flags=re.IGNORECASE
    ),
    "linkedin": re.compile(
        r"\blinkedin\b",
        flags=re.IGNORECASE
    ),
    "github": re.compile(
        r"\bgithub\b",
        flags=re.IGNORECASE
    ),
    "website": re.compile(
        r"\bwebsite\b",
        flags=re.IGNORECASE
    ),
    "how_did_you_hear": re.compile(
        r"\bhow\s+did\s+you\s+hear\b",
        flags=re.IGNORECASE
    ),
    "mailing_address": re.compile(
        r"\bmailing\s*address\b",
        flags=re.IGNORECASE
    ),
    "location_city": re.compile(
        r"\bcity\b",
        flags=re.IGNORECASE
    ),
    "authorized_to_work": re.compile(
        r"\bauthorized\s+to\s+work\b",
        flags=re.IGNORECASE
    ),
    "immigration_sponsorship": re.compile(
        r"\bimmigration\b|\bsponsorship\b",
        flags=re.IGNORECASE
    ),
    "agree": re.compile(
        r"\bagree\b",
        flags=re.IGNORECASE
    ),
    "resume": re.compile(
        r"\bresume\b|\bcv\b",
        flags=re.IGNORECASE
    ),
    "cover_letter": re.compile(
        r"\bcover\s?letter\b",
        flags=re.IGNORECASE
    ),
    "sex": re.compile(
        r"\bsex\b",
        flags=re.IGNORECASE
    ),
    "gender_identity": re.compile(
        r"\b(?=.*\bgender\b)(?=.*(\bidentity\b|\bidentify\b))",
        flags=re.IGNORECASE
    ),
    "transgender": re.compile(
        r"\btransgender\b",
        flags=re.IGNORECASE
    ),
    "sexual_orientation": re.compile(
        r"\bsexual\s+orientation\b",
        flags=re.IGNORECASE
    ),
    "veteran_status": re.compile(
        r"\bveteran\b",
        flags=re.IGNORECASE
    ),
    "disability_status": re.compile(
        r"\bdisability\b",
        flags=re.IGNORECASE
    ),
    "races": re.compile(
        r"\braces\b|\bethnicities\b",
        flags=re.IGNORECASE
    ),
    "ethnicity": re.compile(
        r"\bethnicity\b",
        flags=re.IGNORECASE
    ),
}


def get_question_response(
    question: str,
    personal: ApplyPersonalConfig,
    job_source: JobSource,
    resume_path: str | pathlib.Path,
    cover_letter_path: str | pathlib.Path
) -> str:
    if QUESTION_PATTERNS["fullname"].search(question):
        return f"{personal.first_name} {personal.last_name}"
    elif QUESTION_PATTERNS["firstname"].search(question):
        return personal.first_name
    elif QUESTION_PATTERNS["lastname"].search(question):
        return personal.last_name
    elif QUESTION_PATTERNS["email"].search(question):
        return personal.contact.email_address
    elif QUESTION_PATTERNS["phone"].search(question):
        return personal.contact.phone_number
    elif QUESTION_PATTERNS["linkedin"].search(question):
        return personal.social.linkedin
    elif QUESTION_PATTERNS["github"].search(question):
        return personal.social.github
    elif QUESTION_PATTERNS["website"].search(question):
        return personal.social.website
    elif QUESTION_PATTERNS["how_did_you_hear"].search(question):
        return job_source.shortname
    elif QUESTION_PATTERNS["mailing_address"].search(question):
        return personal.location.to_str(country=False)
    elif QUESTION_PATTERNS["location_city"].search(question):
        return personal.location.to_str(
            street_address=False, zip_code=False, country=False
        )
    elif QUESTION_PATTERNS["authorized_to_work"].search(question):
        return (
            "Yes" if personal.demographic.authorized_to_work else "No"
        )
    elif QUESTION_PATTERNS["immigration_sponsorship"].search(question):
        return (
            "Yes" if personal.demographic.immigration_sponsorship else "No"
        )
    elif QUESTION_PATTERNS["agree"].search(question):
        return "I agree"
    elif QUESTION_PATTERNS["resume"].search(question):
        return str(resume_path)
    elif QUESTION_PATTERNS["cover_letter"].search(question):
        return str(cover_letter_path)
    elif QUESTION_PATTERNS["sexual_orientation"].search(question):
        return personal.demographic.sexual_orientation
    elif QUESTION_PATTERNS["gender_identity"].search(question):
        return personal.demographic.gender
    elif QUESTION_PATTERNS["transgender"].search(question):
        return (
            "Yes" if personal.demographic.transgender else "No"
        )
    elif QUESTION_PATTERNS["disability_status"].search(question):
        return (
            "Yes" if personal.demographic.disability else "No"
        )
    elif QUESTION_PATTERNS["veteran_status"].search(question):
        return (
            "Yes" if personal.demographic.veteran else "No"
        )
    elif QUESTION_PATTERNS["ethnicity"].search(question):
        return personal.demographic.ethnicity
    elif QUESTION_PATTERNS["races"].search(question):
        return Keys.RETURN.join(personal.demographic.races)

    return ""
