<p align="center">
  <img src="https://raw.githubusercontent.com/meilisearch/integration-guides/main/assets/logos/meilisearch_python.svg" alt="Meilisearch-Python" width="200" height="200" />
</p>

<h1 align="center">Meilisearch Python</h1>

<h4 align="center">
  <a href="https://github.com/meilisearch/meilisearch">Meilisearch</a> |
  <a href="https://www.meilisearch.com/cloud?utm_campaign=oss&utm_source=github&utm_medium=meilisearch-python">Meilisearch Cloud</a> |
  <a href="https://www.meilisearch.com/docs">Documentation</a> |
  <a href="https://discord.meilisearch.com">Discord</a> |
  <a href="https://roadmap.meilisearch.com/tabs/1-under-consideration">Roadmap</a> |
  <a href="https://www.meilisearch.com">Website</a> |
  <a href="https://www.meilisearch.com/docs/faq">FAQ</a>
</h4>

<p align="center">
  <a href="https://badge.fury.io/py/meilisearch"><img src="https://badge.fury.io/py/meilisearch.svg" alt="PyPI version"></a>
  <a href="https://github.com/meilisearch/meilisearch-python/actions"><img src="https://github.com/meilisearch/meilisearch-python/workflows/Tests/badge.svg" alt="Test Status"></a>
  <a href="https://github.com/meilisearch/meilisearch-python/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational" alt="License"></a>
  <a href="https://ms-bors.herokuapp.com/repositories/57"><img src="https://bors.tech/images/badge_small.svg" alt="Bors enabled"></a>
</p>

<p align="center">⚡ The Meilisearch API client written for Python 🐍</p>

**Meilisearch Python** is the Meilisearch API client for Python developers.

**Meilisearch** is an open-source search engine. [Learn more about Meilisearch.](https://github.com/meilisearch/meilisearch)

## Table of Contents <!-- omit in TOC -->

- [📖 Documentation](#-documentation)
- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🤖 Compatibility with Meilisearch](#-compatibility-with-meilisearch)
- [💡 Learn more](#-learn-more)
- [⚙️ Contributing](#️-contributing)

## 📖 Documentation

To learn more about Meilisearch Python, refer to the in-depth [Meilisearch Python documentation](https://meilisearch.github.io/meilisearch-python/). To learn more about Meilisearch in general, refer to our [documentation](https://www.meilisearch.com/docs/learn/getting_started/quick_start) or our [API reference](https://www.meilisearch.com/docs/reference/api/overview).

## 🔧 Installation

**Note**: Python 3.8+ is required.

With `pip3` in command line:

```bash
pip3 install meilisearch
```

### Run Meilisearch <!-- omit in toc -->

⚡️ **Launch, scale, and streamline in minutes with Meilisearch Cloud**—no maintenance, no commitment, cancel anytime. [Try it free now](https://cloud.meilisearch.com/login?utm_campaign=oss&utm_source=github&utm_medium=meilisearch-python).

🪨  Prefer to self-host? [Download and deploy](https://www.meilisearch.com/docs/learn/self_hosted/getting_started_with_self_hosted_meilisearch?utm_campaign=oss&utm_source=github&utm_medium=meilisearch-python) our fast, open-source search engine on your own infrastructure.

## 🚀 Getting started

#### Add Documents <!-- omit in toc -->

```python
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')

# An index is where the documents are stored.
index = client.index('movies')

documents = [
      { 'id': 1, 'title': 'Carol', 'genres': ['Romance', 'Drama'] },
      { 'id': 2, 'title': 'Wonder Woman', 'genres': ['Action', 'Adventure'] },
      { 'id': 3, 'title': 'Life of Pi', 'genres': ['Adventure', 'Drama'] },
      { 'id': 4, 'title': 'Mad Max: Fury Road', 'genres': ['Adventure', 'Science Fiction'] },
      { 'id': 5, 'title': 'Moana', 'genres': ['Fantasy', 'Action']},
      { 'id': 6, 'title': 'Philadelphia', 'genres': ['Drama'] },
]

# If the index 'movies' does not exist, Meilisearch creates it when you first add the documents.
index.add_documents(documents) # => { "uid": 0 }
```

With the task `uid`, you can check the status (`enqueued`, `canceled`, `processing`, `succeeded` or `failed`) of your documents addition using the [task](https://www.meilisearch.com/docs/reference/api/tasks#get-tasks).

#### Basic Search <!-- omit in toc -->

```python
# Meilisearch is typo-tolerant:
index.search('caorl')
```

Output:

```json
{
  "hits": [
    {
      "id": 1,
      "title": "Carol",
      "genre": ["Romance", "Drama"]
    }
  ],
  "offset": 0,
  "limit": 20,
  "processingTimeMs": 1,
  "query": "caorl"
}
```

#### Custom Search <!-- omit in toc -->

All the supported options are described in the [search parameters](https://www.meilisearch.com/docs/reference/api/search#search-parameters)

```python
index.search(
  'phil',
  {
    'attributesToHighlight': ['*'],
  }
)
```

JSON output:

```json
{
  "hits": [
    {
      "id": 6,
      "title": "Philadelphia",
      "_formatted": {
        "id": 6,
        "title": "<em>Phil</em>adelphia",
        "genre": ["Drama"]
      }
    }
  ],
  "offset": 0,
  "limit": 20,
  "processingTimeMs": 0,
  "query": "phil"
}
```

#### Custom Search With Filters <!-- omit in toc -->

If you want to enable filtering, you must add your attributes to the `filterableAttributes` index setting.

```py
index.update_filterable_attributes([
  'id',
  'genres'
])
```

#### Custom Serializer for documents <!-- omit in toc -->

If your documents contain fields that the Python JSON serializer does not know how to handle you
can use your own custom serializer.

```py
from datetime import datetime
from json import JSONEncoder
from uuid import uuid4


class CustomEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (UUID, datetime)):
            return str(o)

        # Let the base class default method raise the TypeError
        return super().default(o)


documents = [
    {"id": uuid4(), "title": "test 1", "when": datetime.now()},
    {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
]
index.add_documents(documents, serializer=CustomEncoder)
```

You only need to perform this operation once.

Note that Meilisearch will rebuild your index whenever you update `filterableAttributes`. Depending on the size of your dataset, this might take time. You can track the process using the [task](https://www.meilisearch.com/docs/reference/api/tasks#get-tasks).

Then, you can perform the search:

```py
index.search(
  'wonder',
  {
    'filter': ['id > 1 AND genres = Action']
  }
)
```

```json
{
  "hits": [
    {
      "id": 2,
      "title": "Wonder Woman",
      "genres": ["Action", "Adventure"]
    }
  ],
  "offset": 0,
  "limit": 20,
  "estimatedTotalHits": 1,
  "processingTimeMs": 0,
  "query": "wonder"
}
```

## 🤖 Compatibility with Meilisearch

This package guarantees compatibility with [version v1.2 and above of Meilisearch](https://github.com/meilisearch/meilisearch/releases/latest), but some features may not be present. Please check the [issues](https://github.com/meilisearch/meilisearch-python/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+label%3Aenhancement) for more info.

## 💡 Learn more

The following sections in our main documentation website may interest you:

- **Manipulate documents**: see the [API references](https://www.meilisearch.com/docs/reference/api/documents) or read more about [documents](https://www.meilisearch.com/docs/learn/core_concepts/documents).
- **Search**: see the [API references](https://www.meilisearch.com/docs/reference/api/search).
- **Manage the indexes**: see the [API references](https://www.meilisearch.com/docs/reference/api/indexes) or read more about [indexes](https://www.meilisearch.com/docs/learn/core_concepts/indexes).
- **Configure the index settings**: see the [API references](https://www.meilisearch.com/docs/reference/api/settings) or follow our guide on [settings parameters](https://www.meilisearch.com/docs/learn/configuration/settings).

## ⚙️ Contributing

Any new contribution is more than welcome in this project!

If you want to know more about the development workflow or want to contribute, please visit our [contributing guidelines](/CONTRIBUTING.md) for detailed instructions!

<hr>

**Meilisearch** provides and maintains many **SDKs and Integration tools** like this one. We want to provide everyone with an **amazing search experience for any kind of project**. If you want to contribute, make suggestions, or just know what's going on right now, visit us in the [integration-guides](https://github.com/meilisearch/integration-guides) repository.

## Auto-Launch Feature

When using the Python client with `auto_launch=True`, the client will automatically start a MeiliSearch instance if one is not already running. The port management system ensures:

- If port 0 is specified (`http://localhost:0`), an available port will be automatically assigned
- Port conflicts are handled gracefully with automatic fallback to another available port
- Proper cleanup of port locks when the client is terminated
- Thread-safe port allocation to prevent race conditions

Example:
```python
from meilisearch.client import Client

# Will automatically find an available port
client = Client("http://localhost:0", auto_launch=True)

# Will use port 7700 if available, otherwise find another port
client = Client("http://localhost:7700", auto_launch=True)
```
