from typing import Any

from camel_converter.pydantic_base import CamelBase
from pydantic import ConfigDict


class Webhook(CamelBase):
    """Model for a Meilisearch webhook."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    uuid: str
    url: str
    headers: dict[str, Any] | None = None
    isEditable: bool


class WebhooksResults(CamelBase):
    """Model for webhooks list results."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    results: list[Webhook]
