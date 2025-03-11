class JobSource:
    __shortname: str
    __site: str
    __url: str
    __urn: str

    def __init__(self, shortname: str, site: str, url: str, urn: str):
        self.__shortname = shortname
        self.__site = site
        self.__url = url
        self.__urn = urn

    @property
    def shortname(self) -> str:
        return self.__shortname

    @property
    def site(self) -> str:
        return self.__site

    @property
    def url(self) -> str:
        return self.__url

    @property
    def urn(self) -> str:
        return self.__urn

    def copy(self):
        return type(self)(
            shortname=self.shortname,
            site=self.site,
            url=self.url,
            urn=self.urn
        )
