<p align="center">
  <img src="https://raw.githubusercontent.com/meilisearch/integration-guides/main/assets/logos/meilisearch_python.svg" alt="Meilisearch-Python" width="200" height="200" />
</p>

<h1 align="center">Meilisearch Python</h1>

<h4 align="center">
  <a href="https://github.com/meilisearch/meilisearch">Meilisearch</a> |
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

## Table of Contents <!-- omit in toc -->

- [📖 Documentation](#-documentation)
- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🤖 Compatibility with Meilisearch](#-compatibility-with-meilisearch)
- [💡 Learn more](#-learn-more)
- [⚙️ Contributing](#️-contributing)

## 📖 Documentation

To learn more about Meilisearch Python, refer to the in-depth [Meilisearch Python documentation](https://meilisearch.github.io/meilisearch-python/). To learn more about Meilisearch in general, refer to our [documentation](https://www.meilisearch.com/docs/learn/getting_started/quick_start) or our [API reference](https://www.meilisearch.com/docs/reference/api/overview).

## 🔧 Installation

**Note**: Python 3.7+ is required.

With `pip3` in command line:

```bash
pip3 install meilisearch
```

### Run Meilisearch <!-- omit in toc -->

There are many easy ways to [download and run a Meilisearch instance](https://www.meilisearch.com/docs/learn/getting_started/installation).

For example, using the `curl` command in [your Terminal](https://itconnect.uw.edu/learn/workshops/online-tutorials/what-is-a-terminal/):

```bash
# Install Meilisearch
curl -L https://install.meilisearch.com | sh

# Launch Meilisearch
./meilisearch --master-key=masterKey
```

NB: you can also download Meilisearch from **Homebrew** or **APT** or even run it using **Docker**.

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

With the task `uid`, you can check the status (`enqueued`, `processing`, `succeeded` or `failed`) of your documents addition using the [task](https://www.meilisearch.com/docs/reference/api/tasks#get-tasks).

#### Basic Search <!-- omit in toc -->

``` python
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
      "genres": ["Action","Adventure"]
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

This package guarantees compatibility with [version v1.x of Meilisearch](https://github.com/meilisearch/meilisearch/releases/latest), but some features may not be present. Please check the [issues](https://github.com/meilisearch/meilisearch-python/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+label%3Aenhancement) for more info.

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
