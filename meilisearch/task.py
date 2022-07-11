from urllib import parse
from time import sleep
from datetime import datetime
from typing import Any, Dict, List, Optional

from meilisearch._httprequests import HttpRequests
from meilisearch.config import Config
from meilisearch.errors import MeiliSearchTimeoutError

def get_tasks(config: Config, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Get all tasks.

    Parameters
    ----------
    config:
        Config object containing permission and location of Meilisearch.
    parameters (optional):
        parameters accepted by the get tasks route: https://docs.meilisearch.com/reference/api/tasks.html#get-all-tasks.
        `indexUid` should be set as a List.

    Returns
    -------
    task:
        Dictionary with limit, from, next and results containing a list of all enqueued, processing, succeeded or failed tasks.

    Raises
    ------
    MeiliSearchApiError
        An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
    """
    http = HttpRequests(config)
    if parameters is None:
        parameters = {}
    for param in parameters:
        if isinstance(parameters[param], list):
            parameters[param] = ",".join(parameters[param])
    return http.get(
        f"{config.paths.task}?{parse.urlencode(parameters)}"
    )

def get_task(config: Config, uid: int) -> Dict[str, Any]:
    """Get one task.

    Parameters
    ----------
    config:
        Config object containing permission and location of Meilisearch.
    uid:
        Identifier of the task.
    index_id:
        The id of the `Index`.

    Returns
    -------
    task:
        Dictionary containing information about the status of the asynchronous task.

    Raises
    ------
    MeiliSearchApiError
        An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
    """
    http = HttpRequests(config)
    return http.get(
        f'{config.paths.task}/{uid}'
    )


def wait_for_task(
    config: Config,
    uid: int,
    timeout_in_ms: int = 5000,
    interval_in_ms: int = 50,
) -> Dict[str, Any]:
    """Wait until the task fails or succeeds in Meilisearch.

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
        An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
    """
    start_time = datetime.now()
    elapsed_time = 0.
    while elapsed_time < timeout_in_ms:
        task = get_task(config, uid)
        if task['status'] not in ('enqueued', 'processing'):
            return task
        sleep(interval_in_ms / 1000)
        time_delta = datetime.now() - start_time
        elapsed_time = time_delta.seconds * 1000 + time_delta.microseconds / 1000
    raise MeiliSearchTimeoutError(f'timeout of ${timeout_in_ms}ms has exceeded on process ${uid} when waiting for task to be resolve.')
