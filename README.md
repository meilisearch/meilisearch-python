# Meilisearch Python Client

[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)

The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliDB).</br>
You can also use MeiliSearch as a service by registering on [meilisearch.com](https://www.meilisearch.com/) and use our hosted solution.


## 🔧 Installation



## 🚀 Getting started

Here is a quickstart to create an index and add documents.

```python

```

## 🎬 Examples

You can check out [the API documentation](https://docs.meilisearch.com/references/).

### Search

#### Basic search

```python

```

```json
{
    "hits": [
        {
            "id": 456,
            "title": "Le Petit Prince",
            "_formatted": {
                "id": 456,
                "title": "Le Petit Prince"
            }
        },
        {
            "id": 4,
            "title": "Harry Potter and the Half-Blood Prince",
            "_formatted": {
                "id": 4,
                "title": "Harry Potter and the Half-Blood Prince"
            }
        }
    ],
    "offset": 0,
    "limit": 20,
    "processingTimeMs": 13,
    "query": "prince"
}
```

#### Custom search

All the supported options are described in [this documentation section](https://docs.meilisearch.com/references/search.html#search-in-an-index).

```python

```

```json
{
    "hits": [
        {
            "id": 456,
            "title": "Le Petit Prince",
            "_formatted": {
                "id": 456,
                "title": "Le Petit Prince"
            }
        }
    ],
    "offset": 0,
    "limit": 1,
    "processingTimeMs": 10,
    "query": "prince"
}
```