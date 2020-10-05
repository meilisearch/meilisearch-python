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
  <a href="https://github.com/meilisearch/meilisearch-python/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational" alt="License"></a>
  <a href="https://slack.meilisearch.com"><img src="https://img.shields.io/badge/slack-MeiliSearch-blue.svg?logo=slack" alt="Slack"></a>
</p>

<p align="center">⚡ Lightning Fast, Ultra Relevant, and Typo-Tolerant Search Engine MeiliSearch client written in Python</p>

**MeiliSearch Python** is a client for **MeiliSearch** written in Python. **MeiliSearch** is a powerful, fast, open-source, easy to use and deploy search engine. Both searching and indexing are highly customizable. Features such as typo-tolerance, filters, and synonyms are provided out-of-the-box.

## Table of Contents <!-- omit in toc -->

- [🔧 Installation](#-installation)
- [🚀 Getting started](#-getting-started)
- [🤖 Compatibility with MeiliSearch](#-compatibility-with-meilisearch)
- [📖 Documentation and Examples](#-documentation-and-examples)
- [⚙️ Development Workflow and Contributing](#️-development-workflow-and-contributing)

## 🔧 Installation

With `pip3` in command line:

```bash
$ pip3 install meilisearch
```

### Run MeiliSearch <!-- omit in toc -->

There are many easy ways to [download and run a MeiliSearch instance](https://docs.meilisearch.com/guides/advanced_guides/installation.html#download-and-launch).

For example, if you use Docker:
```bash
$ docker pull getmeili/meilisearch:latest # Fetch the latest version of MeiliSearch image from Docker Hub
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

With the `updateId`, you can check the status (`processed` or `failed`) of your documents addition thanks to this [method](https://docs.meilisearch.com/references/updates.html#get-an-update-status).

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

This package only guarantees the compatibility with the [version v0.15.0 of MeiliSearch](https://github.com/meilisearch/MeiliSearch/releases/tag/v0.15.0).

## 📖 Documentation and Examples

MeiliSearch documentation provides **examples** and a detailed explanation of every one of its features and functionalities, including examples on how to implement them **using this SDK**.

Please read the [guides available in the documentation](https://docs.meilisearch.com/guides/) or check the [API references](https://docs.meilisearch.com/references/) to find the one that you need!

The following sections may interest you:

- [Manipulate documents](https://docs.meilisearch.com/references/documents.html)
- [Search](https://docs.meilisearch.com/references/search.html)
- [Manage the indexes](https://docs.meilisearch.com/references/indexes.html)
- [Configure the index settings](https://docs.meilisearch.com/references/settings.html)

## ⚙️ Development Workflow and Contributing

Any new contribution is more than welcome in this project!

If you want to know more about the development workflow or want to contribute, please visit our [contributing guidelines](/CONTRIBUTING.md) for detailed instructions!

<hr>

**MeiliSearch** provides and maintains many **SDKs and Integration tools** like this one. We want to provide everyone with an **amazing search experience for any kind of project**. If you want to contribute, make suggestions, or just know what's going on right now, visit us in the [integration-guides](https://github.com/meilisearch/integration-guides) repository.
