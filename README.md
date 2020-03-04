# MeiliSearch Python Client

[![PyPI version](https://badge.fury.io/py/meilisearch.svg)](https://badge.fury.io/py/meilisearch)
[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)
[![test Status](https://github.com/meilisearch/meilisearch-python/workflows/Pytest/badge.svg)](https://github.com/{owner}/{repo}/actions)


The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliDB).

Here is the [MeiliSearch documentation](https://docs.meilisearch.com/) 📖

## Table of Contents <!-- omit in toc -->

- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🎬 Examples](#-examples)
  - [Indexes](#indexes)
  - [Documents](#documents)
  - [Update status](#update-status)
  - [Search](#search)
- [🤖 Compatibility with MeiliSearch](#-compatibility-with-meilisearch)

## 🔧 Installation

With `pip3` in command line:

```bash
pip3 install meilisearch
```

### 🏃‍♀️ Run MeiliSearch

There are many easy ways to [download and run a MeiliSearch instance](https://docs.meilisearch.com/guides/advanced_guides/binary.html#download-and-launch).

For example, if you use Docker:
```bash
$ docker run -it --rm -p 7700:7700 getmeili/meilisearch:latest --api-key=apiKey
```

NB: you can also download MeiliSearch from **Homebrew** or **APT**.

## 🚀 Getting started

#### Add documents <!-- omit in toc -->

```python
import meilisearch
client = meilisearch.Client("http://127.0.0.1:7700", "apiKey")
index = client.create_index(name='books', uid='books_uid') # If your index does not exist
index = client.get_index('books_uid') # If you already created your index

documents = [
  { "id": 123,  "title": 'Pride and Prejudice' },
  { "id": 456,  "title": 'Le Petit Prince' },
  { "id": 1,    "title": 'Alice In Wonderland' },
  { "id": 1344, "title": 'The Hobbit' },
  { "id": 4,    "title": 'Harry Potter and the Half-Blood Prince' },
  { "id": 42,   "title": 'The Hitchhiker\'s Guide to the Galaxy' }
]

index.add_documents(documents) # asynchronous
```

#### Search in index <!-- omit in toc -->
``` python
# MeiliSearch is typo-tolerant:
index.search({
  "q": 'hary pottre'
})
```

Output:
```python
{
  "hits" => [{
    "id" => 4,
    "title" => "Harry Potter and the Half-Blood Prince"
  }],
  "offset" => 0,
  "limit" => 20,
  "processingTimeMs" => 1,
  "query" => "hary pottre"
}
```

## 🎬 Examples

You can check out [the API documentation](https://docs.meilisearch.com/references/).

### Indexes

#### Create an index <!-- omit in toc -->
```python
# Create an index
client.create_index(name='Books')
# Create an index with a specific uid (uid must be unique)
client.create_index(name= 'Books', uid= 'books')
# Create an index with a schema
schema = {
  "id":    ["displayed", "indexed", "identifier"],
  "title": ["displayed", "indexed"]
}
client.create_index(name= 'Books', schema= schema)
```

#### List all indexes <!-- omit in toc -->
```python
client.get_indexes()
```

#### Get an index object <!-- omit in toc -->
```python
index = client.get_index(uid="books")
```

### Documents

#### Fetch documents <!-- omit in toc -->
```python
# Get one document
index.get_document(123)
# Get documents by batch
index.get_documents({ "offset": 10 , "limit": 20 })
```
#### Add documents <!-- omit in toc -->
```python
index.add_documents([{ "id": 2, "title": 'Madame Bovary' }])
```

Response:
```json
{
    "updateId": 1
}
```
This `updateId` allows you to [track the current update](#update-status).

#### Delete documents <!-- omit in toc -->
```python
# Delete one document
index.delete_document(2)
# Delete several documents
index.delete_documents([1, 42])
# Delete all documents 
index.delete_all_documents()
```

### Update status
```python
# Get one update
# Parameter: the updateId got after an asynchronous request (e.g. documents addition)
index.get_update(1)
# Get all updates
index.get_updates()
```

### Search

#### Basic search <!-- omit in toc -->

```python
index.search({
  "q": "prince"
})
```

```json
{
    "hits": [
        {
            "id": 456,
            "title": "Le Petit Prince"
        },
        {
            "id": 4,
            "title": "Harry Potter and the Half-Blood Prince"
        }
    ],
    "offset": 0,
    "limit": 20,
    "processingTimeMs": 13,
    "query": "prince"
}
```

#### Custom search <!-- omit in toc -->

All the supported options are described in [this documentation section](https://docs.meilisearch.com/references/search.html#search-in-an-index).

```python
response = index.search({
  "q": "prince",
  "limit": 1
})
```

```json
{
    "hits": [
        {
            "id": 456,
            "title": "Le Petit Prince"
        }
    ],
    "offset": 0,
    "limit": 1,
    "processingTimeMs": 10,
    "query": "prince"
}
```


## 🤖 Compatibility with MeiliSearch

This package works for MeiliSearch `v0.8.x`.
