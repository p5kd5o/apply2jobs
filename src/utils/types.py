from typing import Annotated

from pydantic import BeforeValidator

PY_OBJECT_ID = Annotated[str, BeforeValidator(str)]
