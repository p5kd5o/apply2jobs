from models.job_source import JobSource


class Job:
    __company_name: str
    __title: str
    __description: str
    __apply_url: str
    __source: JobSource

    def __init__(
            self,
            company_name: str,
            title: str,
            description: str,
            apply_url: str,
            source: JobSource
    ):
        self.__company_name = company_name
        self.__title = title
        self.__description = description
        self.__apply_url = apply_url
        self.__source = source.copy()

    @property
    def company_name(self) -> str:
        return self.__company_name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def apply_url(self) -> str:
        return self.__apply_url

    @property
    def source(self) -> JobSource:
        return self.__source
