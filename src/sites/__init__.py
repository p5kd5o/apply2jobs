from importlib import import_module
from pkgutil import iter_modules

from . base import _BaseSearch, _BaseSubmit, _BaseExtract

SITE_CLIENT_TYPE: dict[str, type] = {}

SEARCH_SUPPORTED: dict[str, type[_BaseSearch]] = {}
SUBMIT_SUPPORTED: dict[str, type[_BaseSubmit]] = {}
EXTRACT_SUPPORTED: dict[str, type[_BaseExtract]] = {}

__SITE_MODULE_CLIENT_TYPE_ATTR__: str = "CLIENT_TYPE"

__SITE_MODULE_SUPPORT_CLASS_NAME_MAPPING__: dict[str, str] = {
    "search": "Search",
    "submit": "Submit",
    "extract": "Extract",
}
__SITE_MODULE_SUPPORT_MAPPING__: dict[str, dict] = {
    "search": SEARCH_SUPPORTED,
    "submit": SUBMIT_SUPPORTED,
    "extract": EXTRACT_SUPPORTED,
}


def get_package_site(package: str):
    return ".".join(reversed(package.split(".")[-3:])).replace("_", "-")


def load_supported_modules(path, package, parent=None):
    for module_info in iter_modules(path):
        module_name = module_info.name
        module = import_module(f"{package}.{module_name}")
        if module_info.ispkg:
            if hasattr(module, __SITE_MODULE_CLIENT_TYPE_ATTR__):
                SITE_CLIENT_TYPE[module.SITE] = getattr(
                    module,
                    __SITE_MODULE_CLIENT_TYPE_ATTR__
                )
            load_supported_modules(
                module.__path__, module.__package__, parent=module
            )
        elif module_name in __SITE_MODULE_SUPPORT_MAPPING__:
            if hasattr(
                module,
                __SITE_MODULE_SUPPORT_CLASS_NAME_MAPPING__[module_name]
            ):
                __SITE_MODULE_SUPPORT_MAPPING__[module_name][parent.SITE] = (
                    getattr(
                        module,
                        __SITE_MODULE_SUPPORT_CLASS_NAME_MAPPING__[module_name]
                    )
                )


load_supported_modules(path=__path__, package=__package__)
