import abc

import storage


# pylint: disable=too-few-public-methods
class _BaseService(abc.ABC):
    __backend: storage._BaseBackend

    def __init__(self, backend: storage._BaseBackend):
        self.__backend = backend

    @property
    def backend(self) -> storage._BaseBackend:
        return self.__backend
