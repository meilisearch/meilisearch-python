<p align="center">
  <img src="https://res.cloudinary.com/meilisearch/image/upload/v1587402338/SDKs/meilisearch_python.svg" alt="MeiliSearch-Python" width="200" height="200" />
</p>

<h1 align="center">MeiliSearch Python</h1>

<h4 align="center">
  <a href="https://github.com/meilisearch/MeiliSearch">MeiliSearch</a> |
  <a href="https://www.meilisearch.com">Website</a> |
  <a href="https://blog.meilisearch.com">Blog</a> |
  <a href="https://twitter.com/meilisearch">Twitter</a> |
  <a href="https://docs.meilisearch.com">Documentation</a> |
  <a href="https://docs.meilisearch.com/faq">FAQ</a>
</h4>

<p align="center">
  <a href="https://badge.fury.io/py/meilisearch"><img src="https://badge.fury.io/py/meilisearch.svg" alt="PyPI version"></a>
  <a href="https://github.com/meilisearch/meilisearch-python/actions"><img src="https://github.com/meilisearch/meilisearch-python/workflows/Pytest/badge.svg" alt="Test Status"></a>
  <a href="https://github.com/meilisearch/meilisearch-laravel-scout/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational" alt="License"></a>
  <a href="https://slack.meilisearch.com"><img src="https://img.shields.io/badge/slack-MeiliSearch-blue.svg?logo=slack" alt="Slack"></a>
</p>

<p align="center">⚡ Lightning Fast, Ultra Relevant, and Typo-Tolerant Search Engine MeiliSearch client written in Python</p>

**MeiliSearch Python** is a client for **MeiliSearch** written in Python. **MeiliSearch** is a powerful, fast, open-source, easy to use and deploy search engine. Both searching and indexing are highly customizable. Features such as typo-tolerance, filters, and synonyms are provided out-of-the-box.

## Table of Contents <!-- omit in toc -->

- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🤖 Compatibility with MeiliSearch](#-compatibility-with-meilisearch)
- [🎬 Examples](#-examples)
  - [Indexes](#indexes)
  - [Documents](#documents)
  - [Update status](#update-status)
  - [Search](#search)
- [⚙️ Development Workflow](#️-development-workflow)
  - [Install dependencies](#install-dependencies)
  - [Tests and Linter](#tests-and-linter)
  - [Want to debug?](#want-to-debug)
  - [Release](#release)

## 🔧 Installation

With `pip3` in command line:

```bash
$ pip3 install meilisearch
```

### Run MeiliSearch <!-- omit in toc -->

There are many easy ways to [download and run a MeiliSearch instance](https://docs.meilisearch.com/guides/advanced_guides/installation.html#download-and-launch).

For example, if you use Docker:
```bash
$ docker run -it --rm -p 7700:7700 getmeili/meilisearch:latest ./meilisearch --master-key=masterKey
```

NB: you can also download MeiliSearch from **Homebrew** or **APT**.

## 🚀 Getting started

#### Add documents <!-- omit in toc -->

```python
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')
index = client.create_index('books') # If your index does not exist
index = client.get_index('books')    # If you already created your index

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

## 🤖 Compatibility with MeiliSearch

This package is compatible with the following MeiliSearch versions:
- `v0.11.X`

## 🎬 Examples

You can check out [the API documentation](https://docs.meilisearch.com/references/).

### Indexes

#### Create an index <!-- omit in toc -->
```python
# Create an index
client.create_index('books')
# Create an index and give the primary-key
client.create_index('books', {'primaryKey': 'book_id'})
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
$ docker run -p 7700:7700 getmeili/meilisearch:latest ./meilisearch --master-key=masterKey --no-analytics
$ pipenv run pytest meilisearch
# Linter
$ pipenv run pylint meilisearch
```

### Want to debug?

Import `pdb` in your file and use it:

```python
import pdb

...
pdb.set_trace() # create a break point
...
```

More information [about pdb](https://docs.python.org/3/library/pdb.html).

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

A GitHub Action will be triggered and push the new package on [PyPI](https://pypi.org/project/meilisearch).

<hr>

**MeiliSearch** provides and maintains many **SDKs and Integration tools** like this one. We want to provide everyone with an **amazing search experience for any kind of project**. If you want to contribute, make suggestions, or just know what's going on right now, visit us in the [integration-guides](https://github.com/meilisearch/integration-guides) repository.
