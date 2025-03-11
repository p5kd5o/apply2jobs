from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import Callable, Iterable

import models


SEARCH_SUPPORTED: dict[str, Callable[..., Iterable[models.Job]]] = {}
SUBMIT_SUPPORTED: dict[str, Callable[..., Iterable[models.Job]]] = {}

def populate_supported(path, package, parent=None):
    for module_info in iter_modules(path):
        module = import_module(f"{package}.{module_info.name}")
        if module_info.ispkg:
            populate_supported(
                module.__path__, module.__package__, parent=module
            )
        elif module_info.name == "search":
            SEARCH_SUPPORTED[parent.SITE] = getattr(module, "run")
        elif module_info.name == "submit":
            SUBMIT_SUPPORTED[parent.SITE] = getattr(module, "run")

populate_supported(__path__, __package__)
