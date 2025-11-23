from typing import Any, ClassVar, Self
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BaseModelSingleton(BaseModel):
    _instance: ClassVar[Self | None] = None
    _initalized: ClassVar[bool] = False
    _post_initalized: ClassVar[bool] = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **data: Any) -> None:
        if not self.__class__._initalized:
            super().__init__(**data)
            self.__class__._initalized = True

    def model_post_init(self, context: Any) -> None:
        if not self.__class__._post_initalized:
            super().model_post_init(context)
            self.__class__._post_initalized = True


class BaseSettingsSingleton(BaseSettings):
    _instance: ClassVar[Self | None] = None
    _initalized: ClassVar[bool] = False
    _post_initalized: ClassVar[bool] = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **data: Any) -> None:
        if not self.__class__._initalized:
            super().__init__(**data)
            self.__class__._initalized = True

    def model_post_init(self, context: Any) -> None:
        if not self.__class__._post_initalized:
            super().model_post_init(context)
            self.__class__._post_initalized = True
