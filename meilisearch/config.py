from __future__ import annotations

from typing import Optional, Tuple


class Config:
    """
    Client's credentials and configuration parameters
    """

    class Paths:
        health = "health"
        keys = "keys"
        version = "version"
        index = "indexes"
        task = "tasks"
        stat = "stats"
        search = "search"
        multi_search = "multi-search"
        document = "documents"
        setting = "settings"
        ranking_rules = "ranking-rules"
        distinct_attribute = "distinct-attribute"
        searchable_attributes = "searchable-attributes"
        displayed_attributes = "displayed-attributes"
        stop_words = "stop-words"
        synonyms = "synonyms"
        accept_new_fields = "accept-new-fields"
        filterable_attributes = "filterable-attributes"
        sortable_attributes = "sortable-attributes"
        typo_tolerance = "typo-tolerance"
        dumps = "dumps"
        pagination = "pagination"
        faceting = "faceting"
        swap = "swap-indexes"

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        client_agents: Optional[Tuple[str]] = None,
    ) -> None:
        """
        Parameters
        ----------
        url:
            The url to the Meilisearch API (ex: http://localhost:7700)
        api_key:
            The optional API key to access Meilisearch
        """

        self.url = url
        self.api_key = api_key
        self.timeout = timeout
        self.client_agents = client_agents
        self.paths = self.Paths()
