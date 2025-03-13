from importlib import import_module
from logging import getLogger
from pkgutil import iter_modules
from typing import Callable, Iterable

import models.job

LOGGER = getLogger(__name__)

SEARCH_SUPPORTED: dict[str, Callable[..., Iterable[models.job.Job]]] = {}
SUBMIT_SUPPORTED: dict[str, Callable[..., Iterable[models.job.Job]]] = {}
SITE_CLIENT_TYPE: dict[str, type] = {}

__SITE_MODULE_CLIENT_TYPE_ATTR__: str = "CLIENT_TYPE"
__SITE_MODULE_RUN_MEMBER_NAME__: str = "run"
__SITE_MODULE_SUPPORT_MAPPING__: dict[str, dict] = {
    "search": SEARCH_SUPPORTED,
    "submit": SUBMIT_SUPPORTED,
}


def get_package_site(package: str):
    return ".".join(package.split(".")[-3:][::-1]).replace("_", "-")


def load_supported_modules(path, package, parent=None):
    for module_info in iter_modules(path):
        module_name = module_info.name
        module = import_module(f"{package}.{module_name}")
        if module_info.ispkg:
            if hasattr(module, __SITE_MODULE_CLIENT_TYPE_ATTR__):
                SITE_CLIENT_TYPE[module.SITE] = getattr(
                    module, __SITE_MODULE_CLIENT_TYPE_ATTR__
                )
                LOGGER.info(
                    "Loaded client type for site module: %s: %s",
                    module.__package__,
                    SITE_CLIENT_TYPE[module.SITE]
                )
            load_supported_modules(
                module.__path__, module.__package__, parent=module
            )
        elif module_name in __SITE_MODULE_SUPPORT_MAPPING__:
            if hasattr(module, __SITE_MODULE_RUN_MEMBER_NAME__):
                __SITE_MODULE_SUPPORT_MAPPING__[module_name][parent.SITE] = (
                    getattr(module, __SITE_MODULE_RUN_MEMBER_NAME__)
                )
                LOGGER.info(
                    "Loaded support module: %s",
                    module.__package__
                )
            else:
                LOGGER.warning(
                    "Module missing member ``%s'': %s",
                    __SITE_MODULE_RUN_MEMBER_NAME__,
                    module.__package__
                )


load_supported_modules(path=__path__, package=__package__)
