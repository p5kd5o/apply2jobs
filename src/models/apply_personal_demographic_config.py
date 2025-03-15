from pydantic import BaseModel, Field

CURRENCY_SYMBOLS = """
$¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿⃀
""".strip()


# pylint: disable=too-few-public-methods
class ApplyPersonalDemographicConfig(BaseModel, extra="forbid"):
    desired_salary: str = Field(
        pattern=fr"^[{CURRENCY_SYMBOLS}]?(\d+|\d{{1,3}}([,.]\d{{3}})+)$"
    )
    sex: str
    gender: str
    sexual_orientation: str
    transgender: bool
    citizen: bool
    immigration_sponsorship: bool
    authorized_to_work: bool
    races: list[str]
    ethnicity: str
    disability: bool
    veteran: bool
