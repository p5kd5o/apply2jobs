from importlib import import_module
from logging import getLogger
from pkgutil import iter_modules
from typing import Callable, Iterable

import models.job

LOGGER = getLogger(__name__)

SEARCH_SUPPORTED: dict[str, Callable[..., Iterable[models.job.Job]]] = {}
SUBMIT_SUPPORTED: dict[str, Callable[..., Iterable[models.job.Job]]] = {}

__MODULE_RUN_MEMBER_NAME: str = "run"
__MODULE_SUPPORT_MAPPING: dict[str, dict] = {
    "search": SEARCH_SUPPORTED,
    "submit": SUBMIT_SUPPORTED,
}


def get_package_site(package: str):
    return ".".join(package.split(".")[-3:][::-1]).replace("_", "-")


def load_supported_modules(path, package, parent=None):
    for module_info in iter_modules(path):
        module = import_module(f"{package}.{module_info.name}")
        if module_info.ispkg:
            load_supported_modules(
                module.__path__, module.__package__, parent=module
            )
        elif module_info.name in __MODULE_SUPPORT_MAPPING:
            try:
                __MODULE_SUPPORT_MAPPING[module_info.name][parent.SITE] = (
                    getattr(module, __MODULE_RUN_MEMBER_NAME)
                )
                LOGGER.info(
                    "Loaded support module: %s: %s",
                    module.__package__, module_info.name
                )
            except AttributeError:
                LOGGER.warning(
                    "Module missing ``run'': %s",
                    module.__package__
                )


load_supported_modules(path=__path__, package=__package__)
