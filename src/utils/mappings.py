import operator
from typing import Any, Callable, Mapping, Sequence


def find(
    context: Mapping[Any, Any],
    key: Any,
    compare_func: Callable[[Any, Any], bool] = None
) -> Any:
    if compare_func is None:
        compare_func = operator.eq
    queue = list(context.items())
    while len(queue) > 0:
        item_key, item_value = queue.pop(0)
        if isinstance(item_key, type(key)):
            if compare_func(key, item_key):
                return item_value
        if isinstance(item_value, dict):
            queue.extend(item_value.items())
    raise KeyError(repr(key))


def filter_subset(
    mapping: Mapping[Any, Any],
    keys=Sequence[Any]
) -> dict[Any, Any]:
    to_keep = set(keys)
    return {key: value for key, value in mapping.items() if key in to_keep}
