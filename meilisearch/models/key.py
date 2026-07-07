from datetime import datetime

import pydantic
from camel_converter.pydantic_base import CamelBase

from meilisearch._utils import is_pydantic_2, iso_to_date_time


class _KeyBase(CamelBase):
    uid: str
    name: str | None = None
    description: str | None
    actions: list[str]
    indexes: list[str]
    expires_at: datetime | None = None

    if is_pydantic_2():
        model_config = pydantic.ConfigDict(ser_json_timedelta="iso8601")  # type: ignore[typeddict-unknown-key]

        @pydantic.field_validator("expires_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_expires_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("expires_at", pre=True)
        @classmethod
        def validate_expires_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

        class Config:
            json_encoders = {
                datetime: lambda v: (
                    None
                    if not v
                    else (
                        f"{str(v).split('+', maxsplit=1)[0].replace(' ', 'T')}Z"
                        if "+" in str(v)
                        else f"{str(v).replace(' ', 'T')}Z"
                    )
                )
            }


class Key(_KeyBase):
    key: str
    created_at: datetime
    updated_at: datetime | None = None

    if is_pydantic_2():

        @pydantic.field_validator("created_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_created_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("created_at is required")  # pragma: no cover

            return converted

        @pydantic.field_validator("updated_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_updated_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("created_at", pre=True)
        @classmethod
        def validate_created_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("created_at is required")

            return converted

        @pydantic.validator("updated_at", pre=True)
        @classmethod
        def validate_updated_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)


class KeyUpdate(CamelBase):
    key: str
    name: str | None = None
    description: str | None = None
    actions: list[str] | None = None
    indexes: list[str] | None = None
    expires_at: datetime | None = None

    if is_pydantic_2():
        model_config = pydantic.ConfigDict(ser_json_timedelta="iso8601")  # type: ignore[typeddict-unknown-key]

    else:  # pragma: no cover

        class Config:
            json_encoders = {
                datetime: lambda v: (
                    None
                    if not v
                    else (
                        f"{str(v).split('+', maxsplit=1)[0].replace(' ', 'T')}Z"
                        if "+" in str(v)
                        else f"{str(v).replace(' ', 'T')}Z"
                    )
                )
            }


class KeysResults(CamelBase):
    results: list[Key]
    offset: int
    limit: int
    total: int
