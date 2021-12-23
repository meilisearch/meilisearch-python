from time import sleep
from datetime import datetime
from typing import Any, Dict, List, Optional

from meilisearch._httprequests import HttpRequests
from meilisearch.config import Config
from meilisearch.errors import MeiliSearchTimeoutError

class Task:
    """
    Tasks routes wrapper.

    Task class gives access to all Task routes and child routes via an Index (inherited).
    https://docs.meilisearch.com/reference/api/task.html
    """

    def __init__(
        self,
        config: Config,
        uid: Optional[str] = None,
    ) -> None:
        """
        Parameters
        ----------
        config:
            Config object containing permission and location of MeiliSearch.
        """
        self.config = config
        self.http = HttpRequests(config)
        self.uid = uid

    def get_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tasks.

        Returns
        -------
        task:
            Dictionary containing a list of all enqueued, processing, succeeded or failed tasks.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if self.uid is None:
            return self.http.get(
                f'{self.config.paths.task}'
            )
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.task}'
        )


    def get_task(self, uid: int) -> Dict[str, Any]:
        """Get one task.

        Parameters
        ----------
        uid:
            Identifier of the task.

        Returns
        -------
        task:
            Dictionary containing information about the processed asynchronous task.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if self.uid is None:
            return self.http.get(
                f'{self.config.paths.task}/{uid}'
            )
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.task}/{uid}'
        )


    def wait_for_task(
        self, uid: int,
        timeout_in_ms: int = 5000,
        interval_in_ms: int = 50,
    ) -> Dict[str, Any]:
        """Wait until MeiliSearch processes a task until it fails or succeeds.

        Parameters
        ----------
        uid:
            Identifier of the task to wait for being processed.
        timeout_in_ms (optional):
            Time the method should wait before raising a MeiliSearchTimeoutError.
        interval_in_ms (optional):
            Time interval the method should wait (sleep) between requests.

        Returns
        -------
        task:
            Dictionary containing information about the processed asynchronous task.

        Raises
        ------
        MeiliSearchTimeoutError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        start_time = datetime.now()
        elapsed_time = 0.
        while elapsed_time < timeout_in_ms:
            get_task = self.get_task(uid)
            if get_task['status'] not in ('enqueued', 'processing'):
                return get_task
            sleep(interval_in_ms / 1000)
            time_delta = datetime.now() - start_time
            elapsed_time = time_delta.seconds * 1000 + time_delta.microseconds / 1000
        raise MeiliSearchTimeoutError(f'timeout of ${timeout_in_ms}ms has exceeded on process ${uid} when waiting for task to be resolve.')
