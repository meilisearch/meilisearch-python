import base64
import json
import os
from pathlib import Path

import pytest
import requests

from meilisearch import Client
from meilisearch.errors import MeilisearchApiError
from tests import common

# ---------------- ENV ----------------
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

INDEX_UID = "multi-modal-search-test"
EMBEDDER_NAME = "multimodal"

# ---------------- Paths ----------------
# datasets folder (movies.json)
DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"
MOVIES = json.loads((DATASETS_DIR / "movies.json").read_text())

# fixtures folder (images)
FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


# ---------------- Helper ----------------
def load_image_base64(file_name: str) -> str:
    """
    Load an image from the fixtures folder and return as base64 string.
    """
    file_path = FIXTURES_DIR / file_name
    encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return encoded


# ---------------- Embedder Config ----------------
# Match JS test exactly - fragments have complex nested objects
EMBEDDER_CONFIG = {
    "source": "rest",
    "url": "https://api.voyageai.com/v1/multimodalembeddings",
    "apiKey": VOYAGE_API_KEY,
    "dimensions": 1024,
    "indexingFragments": {
        "textAndPoster": {
            "value": {
                "content": [
                    {
                        "type": "text",
                        "text": "A movie titled {{doc.title}} whose description starts with {{doc.overview|truncatewords:20}}.",
                    },
                    {
                        "type": "image_url",
                        "image_url": "{{doc.poster}}",
                    },
                ],
            },
        },
        "text": {
            "value": {
                "content": [
                    {
                        "type": "text",
                        "text": "A movie titled {{doc.title}} whose description starts with {{doc.overview|truncatewords:20}}.",
                    },
                ],
            },
        },
        "poster": {
            "value": {
                "content": [
                    {
                        "type": "image_url",
                        "image_url": "{{doc.poster}}",
                    },
                ],
            },
        },
    },
    "searchFragments": {
        "textAndPoster": {
            "value": {
                "content": [
                    {
                        "type": "text",
                        "text": "{{media.textAndPoster.text}}",
                    },
                    {
                        "type": "image_base64",
                        "image_base64": "data:{{media.textAndPoster.image.mime}};base64,{{media.textAndPoster.image.data}}",
                    },
                ],
            },
        },
        "text": {
            "value": {
                "content": [
                    {
                        "type": "text",
                        "text": "{{media.text.text}}",
                    },
                ],
            },
        },
        "poster": {
            "value": {
                "content": [
                    {
                        "type": "image_url",
                        "image_url": "{{media.poster.poster}}",
                    },
                ],
            },
        },
    },
    "request": {
        "inputs": ["{{fragment}}", "{{..}}"],
        "model": "voyage-multimodal-3",
    },
    "response": {
        "data": [
            {
                "embedding": "{{embedding}}",
            },
            "{{..}}",
        ],
    },
}


# ---------------- Tests ----------------
@pytest.mark.skipif(not VOYAGE_API_KEY, reason="Voyage API key not set")
class TestMultimodalSearch:
    """Multi-modal search tests"""

    # Class attribute populated by setup_index fixture
    search_client: Client

    @pytest.fixture(autouse=True)
    def clear_indexes(self, client):
        """
        Override the global clear_indexes fixture to exclude the multimodal test index.
        This prevents the index from being deleted between tests in this class.
        """
        yield
        # Delete all indexes except the multimodal test index
        indexes = client.get_indexes()
        for index in indexes["results"]:
            if index.uid != INDEX_UID:
                try:
                    task = client.index(index.uid).delete()
                    client.wait_for_task(task.task_uid)
                except (MeilisearchApiError, Exception):  # pylint: disable=broad-exception-caught
                    # Ignore errors when deleting indexes (may not exist)
                    pass

    @pytest.fixture(scope="class", autouse=True)
    def setup_index(self, request):
        """Setup index with embedder configuration."""
        client = Client(common.BASE_URL, common.MASTER_KEY)

        # Enable multimodal experimental feature
        client.update_experimental_features({"multimodal": True})

        # Delete the index if it already exists
        try:
            task = client.index(INDEX_UID).delete()
            client.wait_for_task(task.task_uid)
        except MeilisearchApiError:
            pass  # Index doesn't exist, which is fine

        # Create index
        task = client.create_index(INDEX_UID)
        client.wait_for_task(task.task_uid)

        # Update settings with embedder config
        # Use raw HTTP request because fragments with complex objects
        # may not pass Pydantic validation
        settings_payload = {
            "searchableAttributes": ["title", "overview"],
            "embedders": {
                EMBEDDER_NAME: EMBEDDER_CONFIG,
            },
        }

        response = requests.patch(
            f"{common.BASE_URL}/indexes/{INDEX_UID}/settings",
            headers={
                "Authorization": f"Bearer {common.MASTER_KEY}",
                "Content-Type": "application/json",
            },
            json=settings_payload,
            timeout=30,
        )
        response.raise_for_status()

        # Wait for settings update task (embedder config can take longer)
        task_data = response.json()
        task_uid = task_data.get("taskUid")
        client.wait_for_task(task_uid, timeout_in_ms=60_000)

        index = client.get_index(INDEX_UID)

        # Add documents
        task = index.add_documents(MOVIES)
        # Use longer timeout for document indexing with embeddings
        # Each document needs embeddings generated via Voyage API, which can be slow
        client.wait_for_task(
            task.task_uid,
            timeout_in_ms=300_000,  # 5 minutes timeout for embedding generation
            interval_in_ms=1000,  # Poll every 1 second instead of 50ms to reduce log noise
        )

        # Verify index is ready by checking stats
        stats = index.get_stats()
        assert stats.number_of_documents == len(
            MOVIES
        ), f"Expected {len(MOVIES)} documents, got {stats.number_of_documents}"

        # Store for tests on the class
        # Use request.cls to ensure attributes are available on test instances
        request.cls.search_client = client

    def test_text_query(self):
        """Test text query search"""
        query = "The story follows Carol Danvers"
        response = self.search_client.index(INDEX_UID).search(
            query,
            {
                "media": {
                    "text": {
                        "text": query,
                    },
                },
                "hybrid": {
                    "embedder": EMBEDDER_NAME,
                    "semanticRatio": 1,
                },
            },
        )
        assert response["hits"][0]["title"] == "Captain Marvel"

    def test_image_query(self):
        """Test image query search"""
        # Find Dumbo in the movies list
        dumbo_movie = next(m for m in MOVIES if m["title"] == "Dumbo")
        dumbo_poster = dumbo_movie["poster"]

        response = self.search_client.index(INDEX_UID).search(
            None,
            {
                "media": {
                    "poster": {
                        "poster": dumbo_poster,
                    },
                },
                "hybrid": {
                    "embedder": EMBEDDER_NAME,
                    "semanticRatio": 1,
                },
            },
        )
        assert response["hits"][0]["title"] == "Dumbo"

    def test_text_and_image_query(self):
        """Test text and image query"""
        query = "a futuristic movie"
        master_yoda_base64 = load_image_base64("master-yoda.jpeg")

        response = self.search_client.index(INDEX_UID).search(
            None,
            {
                "q": query,
                "media": {
                    "textAndPoster": {
                        "text": query,
                        "image": {
                            "mime": "image/jpeg",
                            "data": master_yoda_base64,
                        },
                    },
                },
                "hybrid": {
                    "embedder": EMBEDDER_NAME,
                    "semanticRatio": 1,
                },
            },
        )
        assert response["hits"][0]["title"] == "Captain Marvel"
