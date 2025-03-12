import operator
from typing import Any, Callable


def find(
    context: dict[Any, Any],
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
