# MeiliSearch Python Client

[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)

The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliDB).

Here is the [MeiliSearch documentation](https://docs.meilisearch.com/) 📖

# 🔧 Installation

```bash
pip install meilisearch==0.8.0
```

## Quickstart
```bash
import meilisearch
client = meilisearch.Client("http://127.0.0.1:7700", "123")
indexes = client.get_indexes()
```

# Contributing 

##  Installation

```bash
pipenv install
pipenv shell
pytest
```

## Linting
```bash
pylint meilisearch
pylint tests/*
```

## Generate documentation
```bash
pdoc3 meilisearch --html
```
