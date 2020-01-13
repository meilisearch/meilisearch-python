# MeiliSearch Python Client

[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)

The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliDB).

Here is the [MeiliSearch documentation](https://docs.meilisearch.com/) 📖

# 🔧 Installation

```bash
pip install meilisearch==0.8.0
```

### 🏃‍♀️ Run MeiliSearch

There are many easy ways to download and run a MeiliSearch instance.</br>

For example, if you use Docker:
```bash
$ docker run -it --rm -p 7700:7700 getmeili/meilisearch:latest --api-key=apiKey
```

NB: you can also download MeiliSearch from **Homebrew** or **APT**.

## Quickstart
```bash
import meilisearch
client = meilisearch.Client("http://127.0.0.1:7700", "123")
indexes = client.get_indexes()
```

# Contributing

## Installation

```bash
pipenv install --dev
pipenv shell
```

## Testing

```bash
pipenv install --dev
pipenv run pytest
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
