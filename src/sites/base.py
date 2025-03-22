import abc
import pathlib
from typing import Callable, Any

from mistralai import Mistral
from selenium.webdriver.remote.webdriver import WebDriver

from models import Job, ApplyPersonalConfig


# pylint: disable=too-few-public-methods
class _BaseSearch(abc.ABC):
    client: Any

    def __init__(self, client: Any):
        super().__init__()
        self.client = client

    @abc.abstractmethod
    def main(self, **search_kwgs):
        pass

    def __call__(self, *args, **kwgs):
        return self.main(*args, **kwgs)


# pylint: disable=too-few-public-methods
class _BaseSubmit(abc.ABC):
    webdriver: WebDriver
    mistral_client: Mistral
    pre_submit_hook: list[Callable[[], Any]] = None

    def __init__(
        self,
        webdriver: WebDriver,
        mistral_client: Mistral,
        pre_submit_hook: list[Callable[[], Any]] = None
    ):
        super().__init__()
        self.webdriver = webdriver
        self.mistral_client = mistral_client
        if pre_submit_hook is None:
            self.pre_submit_hook = []
        else:
            self.pre_submit_hook = list(pre_submit_hook)

    @abc.abstractmethod
    def main(
        self,
        job: Job,
        personal: ApplyPersonalConfig,
        resume_path: str | pathlib.Path,
        cover_letter_dir: str | pathlib.Path
    ) -> None:
        pass

    def __call__(self, *args, **kwgs):
        return self.main(*args, **kwgs)
