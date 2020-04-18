# MeiliSearch Python Client <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/meilisearch.svg)](https://badge.fury.io/py/meilisearch)
[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)
[![test Status](https://github.com/meilisearch/meilisearch-python/workflows/Pytest/badge.svg)](https://github.com/{owner}/{repo}/actions)

The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliSearch).

Here is the [MeiliSearch documentation](https://docs.meilisearch.com/) 📖

## Table of Contents <!-- omit in toc -->

- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🎬 Examples](#-examples)
  - [Indexes](#indexes)
  - [Documents](#documents)
  - [Update status](#update-status)
  - [Search](#search)
- [⚙️ Development Workflow](#️-development-workflow)
  - [Install dependencies](#install-dependencies)
  - [Tests and Linter](#tests-and-linter)
  - [Release](#release)
- [🤖 Compatibility with MeiliSearch](#-compatibility-with-meilisearch)

## 🔧 Installation

With `pip3` in command line:

```bash
$ pip3 install meilisearch
```

### Run MeiliSearch <!-- omit in toc -->

There are many easy ways to [download and run a MeiliSearch instance](https://docs.meilisearch.com/guides/advanced_guides/installation.html#download-and-launch).

For example, if you use Docker:
```bash
$ docker run -it --rm -p 7700:7700 getmeili/meilisearch:latest --master-key=masterKey
```

NB: you can also download MeiliSearch from **Homebrew** or **APT**.

## 🚀 Getting started

#### Add documents <!-- omit in toc -->

```python
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')
index = client.create_index(uid='books') # If your index does not exist
index = client.get_index('books')        # If you already created your index

documents = [
  { 'book_id': 123,  'title': 'Pride and Prejudice' },
  { 'book_id': 456,  'title': 'Le Petit Prince' },
  { 'book_id': 1,    'title': 'Alice In Wonderland' },
  { 'book_id': 1344, 'title': 'The Hobbit' },
  { 'book_id': 4,    'title': 'Harry Potter and the Half-Blood Prince' },
  { 'book_id': 42,   'title': 'The Hitchhiker\'s Guide to the Galaxy' }
]

index.add_documents(documents) # => { "updateId": 0 }
```

With the `updateId`, you can check the status (`processed` or `failed`) of your documents addition thanks to this [method](#update-status).

#### Search in index <!-- omit in toc -->
``` python
# MeiliSearch is typo-tolerant:
index.search('harry pottre')
```

Output:
```python
{
  "hits" => [{
    "book_id" => 4,
    "title" => "Harry Potter and the Half-Blood Prince"
  }],
  "offset" => 0,
  "limit" => 20,
  "processingTimeMs" => 1,
  "query" => "harry pottre"
}
```

## 🎬 Examples

You can check out [the API documentation](https://docs.meilisearch.com/references/).

### Indexes

#### Create an index <!-- omit in toc -->
```python
# Create an index
client.create_index(uid='books')
# Create an index and give the primary-key
client.create_index(uid='books', primary_key='book_id')
```

#### List all indexes <!-- omit in toc -->
```python
client.get_indexes()
```

#### Get an index object <!-- omit in toc -->

```python
index = client.get_index('books')
```

### Documents

#### Fetch documents <!-- omit in toc -->

```python
# Get one document
index.get_document(123)
# Get documents by batch
index.get_documents({ 'offset': 10 , 'limit': 20 })
```

#### Add documents <!-- omit in toc -->

```python
index.add_documents([{ 'book_id': 2, 'title': 'Madame Bovary' }])
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
# Get one update status
# Parameter: the updateId got after an asynchronous request (e.g. documents addition)
index.get_update_status(1)
# Get all updates status
index.get_all_update_status()
```

### Search

#### Basic search <!-- omit in toc -->

```python
index.search('prince')
```

```json
{
    "hits": [
        {
            "book_id": 456,
            "title": "Le Petit Prince"
        },
        {
            "book_id": 4,
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
response = index.search('prince', { 'limit': 1 })
```

```json
{
    "hits": [
        {
            "book_id": 456,
            "title": "Le Petit Prince"
        }
    ],
    "offset": 0,
    "limit": 1,
    "processingTimeMs": 10,
    "query": "prince"
}
```

## ⚙️ Development Workflow

If you want to contribute, this section describes the steps to follow.

Thank you for your interest in a MeiliSearch tool! ♥️

### Install dependencies

```bash
$ pipenv install --dev
```

### Tests and Linter

Each PR should pass the tests and the linter to be accepted.

```bash
# Tests
$ docker run -d -p 7700:7700 getmeili/meilisearch:latest ./meilisearch --master-key=masterKey --no-analytics
$ pipenv run pytest meilisearch
# Linter
$ pipenv run pylint meilisearch
```

### Release

MeiliSearch tools follow the [Semantic Versioning Convention](https://semver.org/).

You must do a PR modifying the file `setup.py` with the right version.<br>

```python
version="X.X.X"
```

Once the changes are merged on `master`, in your terminal, you must be on the `master` branch and push a new tag with the right version:

```bash
$ git checkout master
$ git pull origin master
$ git tag vX.X.X
$ git push --tag origin master
```

A GitHub Action will be triggered and push the new gem on [RubyGems](https://rubygems.org/gems/meilisearch).

## 🤖 Compatibility with MeiliSearch

This package works for MeiliSearch `>=v0.10`.
