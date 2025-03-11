from importlib import import_module
from pkgutil import iter_modules
from typing import Callable, Iterable

import models

SEARCH_SUPPORTED: dict[str, Callable[..., Iterable[models.Job]]] = {}
SUBMIT_SUPPORTED: dict[str, Callable[..., Iterable[models.Job]]] = {}

(lambda y: y(y))(
    lambda x, path=__path__, package=__package__, parent=None: [
        (
            lambda module, module_info=module_info:
            x(x, module.__path__, module.__package__, parent=module)
            if module_info.ispkg
            else SEARCH_SUPPORTED.setdefault(parent.SITE, getattr(module, "run"))
            if module_info.name == "search"
            else SUBMIT_SUPPORTED.setdefault(parent.SITE, getattr(module, "run"))
            if module_info.name == "submit"
            else ""
        )(import_module(f"{package}.{module_info.name}"))
        for module_info in iter_modules(path)
    ]
)
