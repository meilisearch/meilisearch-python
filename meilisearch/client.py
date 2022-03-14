import base64
import hashlib
import hmac
import json
import datetime
from typing import Any, Dict, List, Optional, Union
from meilisearch.index import Index
from meilisearch.config import Config
from meilisearch.task import get_task, get_tasks, wait_for_task
from meilisearch._httprequests import HttpRequests
from meilisearch.errors import MeiliSearchError

class Client():
    """
    A client for the Meilisearch API

    A client instance is needed for every Meilisearch API method to know the location of
    Meilisearch and its permissions.
    """

    def __init__(
        self, url: str, api_key: Optional[str] = None, timeout: Optional[int] = None
    ) -> None:
        """
        Parameters
        ----------
        url:
            The url to the Meilisearch API (ex: http://localhost:7700)
        api_key:
            The optional API key for Meilisearch
        """
        self.config = Config(url, api_key, timeout=timeout)

        self.http = HttpRequests(self.config)

    def create_index(self, uid: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create an index.

        Parameters
        ----------
        uid: str
            UID of the index.
        options (optional): dict
            Options passed during index creation (ex: primaryKey).

        Returns
        -------
        task:
            Dictionary containing a task to track the informations about the progress of an asynchronous process.
            https://docs.meilisearch.com/reference/api/tasks.html#get-one-task

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return Index.create(self.config, uid, options)

    def delete_index(self, uid: str) -> Dict[str, Any]:
        """Deletes an index

        Parameters
        ----------
        uid:
            UID of the index.

        Returns
        -------
        task:
            Dictionary containing a task to track the informations about the progress of an asynchronous process.
            https://docs.meilisearch.com/reference/api/tasks.html#get-one-task

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """

        return self.http.delete(f'{self.config.paths.index}/{uid}')

    def get_indexes(self) -> List[Index]:
        """Get all indexes.

        Returns
        -------
        indexes:
            List of Index instances.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        response = self.http.get(self.config.paths.index)

        return [
            Index(
                self.config,
                index["uid"],
                index["primaryKey"],
                index["createdAt"],
                index["updatedAt"],
            )
            for index in response
        ]

    def get_raw_indexes(self) -> List[Dict[str, Any]]:
        """Get all indexes in dictionary format.

        Returns
        -------
        indexes:
            List of indexes in dictionary format. (e.g [{ 'uid': 'movies' 'primaryKey': 'objectID' }])

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.index)

    def get_index(self, uid: str) -> Index:
        """Get the index.
        This index should already exist.

        Parameters
        ----------
        uid:
            UID of the index.

        Returns
        -------
        index:
            An Index instance containing the information of the fetched index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return Index(self.config, uid).fetch_info()

    def get_raw_index(self, uid: str) -> Dict[str, Any]:
        """Get the index as a dictionary.
        This index should already exist.

        Parameters
        ----------
        uid:
            UID of the index.

        Returns
        -------
        index:
            An index in dictionary format. (e.g { 'uid': 'movies' 'primaryKey': 'objectID' })

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(f'{self.config.paths.index}/{uid}')

    def index(self, uid: str) -> Index:
        """Create a local reference to an index identified by UID, without doing an HTTP call.
        Calling this method doesn't create an index in the Meilisearch instance, but grants access to all the other methods in the Index class.

        Parameters
        ----------
        uid:
            UID of the index.

        Returns
        -------
        index:
            An Index instance.
        """
        if uid is not None:
            return Index(self.config, uid=uid)
        raise Exception('The index UID should not be None')

    def get_all_stats(self) -> Dict[str, Any]:
        """Get all stats of Meilisearch

        Get information about database size and all indexes
        https://docs.meilisearch.com/reference/api/stats.html

        Returns
        -------
        stats:
            Dictionary containing stats about your Meilisearch instance.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.stat)

    def health(self) -> Dict[str, str]:
        """Get health of the Meilisearch server.

        Returns
        -------
        health:
            Dictionary containing the status of the Meilisearch instance.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.health)

    def is_healthy(self) -> bool:
        """Get health of the Meilisearch server.
        """
        try:
            self.health()
        except MeiliSearchError:
            return False
        return True

    def get_key(self, key: str) -> Dict[str, Any]:
        """Gets information about a specific API key.

        Parameters
        ----------
        key:
            The key for which to retrieve the information.

        Returns
        -------
        key:
            The API key.
            https://docs.meilisearch.com/reference/api/keys.html#get-key

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(f'{self.config.paths.keys}/{key}')

    def get_keys(self) -> Dict[str, Any]:
        """Gets the Meilisearch API keys.

        Returns
        -------
        keys:
            API keys.
            https://docs.meilisearch.com/reference/api/keys.html#get-keys

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.keys)

    def create_key(
        self,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Creates a new API key.

        Parameters
        ----------
        options:
            Options, the information to use in creating the key (ex: { 'actions': ['*'], 'indexes': ['movies'], 'description': 'Search Key', 'expiresAt': '22-01-01' }).
            An `actions`, an `indexes` and a `expiresAt` fields are mandatory,`None` should be specified for no expiration date.
            `actions`: A list of actions permitted for the key. ["*"] for all actions.
            `indexes`: A list of indexes permitted for the key. ["*"] for all indexes.
            Note that if an expires_at value is included it should be in UTC time.

        Returns
        -------
        keys:
            The new API key.
            https://docs.meilisearch.com/reference/api/keys.html#get-keys

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(f'{self.config.paths.keys}', options)

    def update_key(
        self,
        key: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an API key.

        Parameters

        ----------
        key:
            The key for which to update the information.
        options:
            The information to use in creating the key (ex: { 'description': 'Search Key', 'expiresAt': '22-01-01' }). Note that if an
            expires_at value is included it should be in UTC time.

        Returns
        -------
        key:
            The updated API key.
            https://docs.meilisearch.com/reference/api/keys.html#get-keys

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        url = f'{self.config.paths.keys}/{key}'
        return self.http.patch(url, options)

    def delete_key(self, key: str) -> Dict[str, int]:
        """Deletes an API key.

        Parameters
        ----------
        key:
            The key to delete.

        Returns
        -------
        keys:
            The Response status code. 204 signifies a successful delete.
            https://docs.meilisearch.com/reference/api/keys.html#get-keys

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(f'{self.config.paths.keys}/{key}')

    def get_version(self) -> Dict[str, str]:
        """Get version Meilisearch

        Returns
        -------
        version:
            Information about the version of Meilisearch.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.version)

    def version(self) -> Dict[str, str]:
        """Alias for get_version

        Returns
        -------
        version:
            Information about the version of Meilisearch.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.get_version()

    def create_dump(self) -> Dict[str, str]:
        """Trigger the creation of a Meilisearch dump.

        Returns
        -------
        Dump:
            Information about the dump.
            https://docs.meilisearch.com/reference/api/dump.html#create-a-dump

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(self.config.paths.dumps)

    def get_dump_status(self, uid: str) -> Dict[str, str]:
        """Retrieve the status of a Meilisearch dump creation.

        Parameters
        ----------
        uid:
            UID of the dump.

        Returns
        -------
        Dump status:
            Information about the dump status.
            https://docs.meilisearch.com/reference/api/dump.html#get-dump-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.config.paths.dumps + '/' + str(uid) + '/status'
        )

    def get_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tasks.

        Returns
        -------
        task:
            Dictionary containing a list of all enqueued, processing, succeeded or failed tasks.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return get_tasks(self.config)

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
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return get_task(self.config, uid)

    def wait_for_task(
        self, uid: int,
        timeout_in_ms: int = 5000,
        interval_in_ms: int = 50,
    ) -> Dict[str, Any]:
        """Wait until Meilisearch processes a task until it fails or succeeds.

        Parameters
        ----------
        uid:
            Identifier of the task to wait for being processed.
        timeout_in_ms (optional):
            Time the method should wait before raising a MeiliSearchTimeoutError
        interval_in_ms (optional):
            Time interval the method should wait (sleep) between requests

        Returns
        -------
        task:
            Dictionary containing information about the processed asynchronous task.

        Raises
        ------
        MeiliSearchTimeoutError
            An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return wait_for_task(self.config, uid, timeout_in_ms, interval_in_ms)

    def generate_tenant_token(
        self,
        search_rules: Union[Dict[str, Any], List[str]],
        *,
        expires_at: Optional[datetime.datetime] = None,
        api_key: Optional[str] = None
    ) -> str:
        """Generate a JWT token for the use of multitenancy.

        Parameters
        ----------
        search_rules:
            A Dictionary or list of string which contains the rules to be enforced at search time for all or specific
            accessible indexes for the signing API Key.
            In the specific case where you do not want to have any restrictions you can also use a list ["*"].
        expires_at (optional):
            Date and time when the key will expire. Note that if an expires_at value is included it should be in UTC time.
        api_key (optional):
            The API key parent of the token. If you leave it empty the client API Key will be used.

        Returns
        -------
        jwt_token:
           A string containing the jwt tenant token.
           Note: If your token does not work remember that the search_rules is mandatory and should be well formatted.
           `exp` must be a `datetime` in the future. It's not possible to create a token from the master key.
        """
        # Validate all fields
        if api_key == '' or api_key is None and self.config.api_key is None:
            raise Exception('An api key is required in the client or should be passed as an argument.')
        if not search_rules or search_rules == ['']:
            raise Exception('The search_rules field is mandatory and should be defined.')
        if expires_at and expires_at < datetime.datetime.utcnow():
            raise Exception('The date expires_at should be in the future.')

        # Standard JWT header for encryption with SHA256/HS256 algorithm
        header = {
            "typ": "JWT",
            "alg": "HS256"
        }

        api_key = str(self.config.api_key) if api_key is None else api_key

        # Add the required fields to the payload
        payload = {
            'apiKeyPrefix': api_key[0:8],
            'searchRules': search_rules,
            'exp': int(datetime.datetime.timestamp(expires_at)) if expires_at is not None else None
        }

        # Serialize the header and the payload
        json_header = json.dumps(header, separators=(",",":")).encode()
        json_payload = json.dumps(payload, separators=(",",":")).encode()

        # Encode the header and the payload to Base64Url String
        header_encode = self._base64url_encode(json_header)
        payload_encode = self._base64url_encode(json_payload)

        secret_encoded = api_key.encode()
        # Create Signature Hash
        signature = hmac.new(secret_encoded, (header_encode + "." + payload_encode).encode(), hashlib.sha256).digest()
        # Create JWT
        jwt_token = header_encode + '.' + payload_encode + '.' + self._base64url_encode(signature)

        return jwt_token

    @staticmethod
    def _base64url_encode(
        data: bytes
    ) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').replace('=','')
