import re

QUESTION_PATTERN_FIRSTNAME = re.compile(
    r"\bfirst\s?name\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_LASTNAME = re.compile(
    r"\blast\s?name\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_FULLNAME = re.compile(
    r"\bfull\s?name\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_EMAIL = re.compile(
    r"\be-?mail\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_PHONE = re.compile(
    r"\bphone\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_LINKEDIN = re.compile(
    r"\blinkedin\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_GITHUB = re.compile(
    r"\bgithub\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_WEBSITE = re.compile(
    r"\bwebsite\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_HOW_DID_YOU_HEAR = re.compile(
    r"\bhow\s+did\s+you\s+hear\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_MAILING_ADDRESS = re.compile(
    r"\bmailing\s*address\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_LOCATION_CITY = re.compile(
    r"\bcity\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_SALARY = re.compile(
    r"\b(pay|salary)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_AUTHORIZED_TO_WORK = re.compile(
    r"\bauthorized\s+to\s+work\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_IMMIGRATION_SPONSORSHIP = re.compile(
    r"\b(immigration|sponsorship)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_AGREE = re.compile(
    r"\b(acknowledge|agree)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_RESUME = re.compile(
    r"\b(resume|cv)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_COVER_LETTER = re.compile(
    r"\bcover\s?letter\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_GENDER_IDENTITY = re.compile(
    r"(?=.*\bgender\b)(?=.*\b(identity|identify)\b)",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_TRANSGENDER = re.compile(
    r"\btransgender\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_SEX_GENDER = re.compile(
    r"\b(sex|gender)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_PRONOUNS = re.compile(
    r"\bpronouns\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_SEXUAL_ORIENTATION = re.compile(
    r"\bsexual\s+orientation\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_VETERAN_STATUS = re.compile(
    r"\bveteran\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_DISABILITY_STATUS = re.compile(
    r"\bdisability\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_RACES = re.compile(
    r"\b(races|ethnicities)\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_ETHNICITY = re.compile(
    r"\bethnicity\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_HISPANIC_LATINO = re.compile(
    r"\bhispanic\b",
    flags=re.IGNORECASE
)
QUESTION_PATTERN_UNITED_STATES = re.compile(
    r"\b(united\s+states|u\.?s\.?a\.?)\b",
    flags=re.IGNORECASE
)
