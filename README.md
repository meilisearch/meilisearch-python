# Meilisearch Python Client

[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://img.shields.io/badge/licence-MIT-blue.svg)

The python client for MeiliSearch API.

MeiliSearch provides an ultra relevant and instant full-text search. Our solution is open-source and you can check out [our repository here](https://github.com/meilisearch/MeiliDB).</br>
You can also use MeiliSearch as a service by registering on [meilisearch.com](https://www.meilisearch.com/) and use our hosted solution.



# Using alpha release

### pipenv
```bash
pipenv install --pypi-mirror 'https://test.pypi.org/simple/' meilisearch==0.0.7
```
### pip
```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps meilisearch==0.0.7

```

## Quickstart
```bash
import meilisearch
client = meilisearch.Client("http://127.0.0.1:7700", "123")
indexes = client.get_indexes()
```

# Contributing 

## 🔧 Installation

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
