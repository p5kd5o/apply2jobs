import dataclasses
import re


@dataclasses.dataclass
class SearchRE:
    value: str
    flags: re.RegexFlag = re.NOFLAG

    def __eq__(self, pattern: re.Pattern | str):
        if isinstance(pattern, str):
            pattern = re.compile(pattern, flags=self.flags)
        return pattern.search(string=self.value) is not None
