from functools import partial
from typing import cast

from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict as _SettingsConfigDict


class BaseConfig(_BaseSettings): ...


BaseSettingsConfigDict: _SettingsConfigDict = cast(
    _SettingsConfigDict,
    partial(
        _SettingsConfigDict,
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
    ),
)