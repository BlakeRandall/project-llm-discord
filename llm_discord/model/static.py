from typing import Any


class StaticMeta(type):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError(
            f"class, {cls.__name__},(metaclass={cls.__class__.__class__}) should not be instatited"
        )
