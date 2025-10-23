# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏗️ Project Overview

This is the **Meilisearch Python SDK** - the official Python client library for the Meilisearch search engine. It provides a complete Python interface for all Meilisearch API operations including document management, search, index configuration, and administrative tasks.

## 🚀 Development Commands

### Environment Setup
```bash
# Install dependencies
pipenv install --dev

# Activate virtual environment
pipenv shell
```

### Testing
```bash
# Start Meilisearch server (required for tests)
curl -L https://install.meilisearch.com | sh
./meilisearch --master-key=masterKey --no-analytics

# Run all tests
pipenv run pytest tests

# Run tests with coverage
pipenv run pytest tests --cov=meilisearch --cov-report term-missing

# Run specific test file
pipenv run pytest tests/client/test_client.py

# Run with Docker (alternative)
docker pull getmeili/meilisearch:latest
docker run -p 7700:7700 getmeili/meilisearch:latest meilisearch --master-key=masterKey --no-analytics
```

### Code Quality
```bash
# Type checking
pipenv run mypy meilisearch

# Linting
pipenv run pylint meilisearch tests

# Code formatting
pipenv run black meilisearch tests
pipenv run isort meilisearch tests
```

### Testing All Python Versions
```bash
# Using tox (runs tests on all supported Python versions)
pipenv run tox
```

### Docker Development
```bash
# Run all checks with docker
docker-compose run --rm package bash -c "pipenv install --dev && pipenv run mypy meilisearch && pipenv run pylint meilisearch tests && pipenv run pytest tests"
```

## 🏛️ Architecture Overview

### Core Structure
- **`meilisearch/client.py`**: Main `Client` class - entry point for all API operations
- **`meilisearch/index.py`**: `Index` class - handles index-specific operations (search, documents, settings)
- **`meilisearch/task.py`**: Task management and waiting utilities
- **`meilisearch/_httprequests.py`**: HTTP request handling and error management
- **`meilisearch/models/`**: Pydantic models for API responses and configuration

### API Client Pattern
The SDK follows a hierarchical client pattern:
```python
# Client -> Index -> Operations
client = meilisearch.Client('http://localhost:7700', 'masterKey')
index = client.index('movies')
results = index.search('query')
```

### Key Design Patterns
1. **Async Task Handling**: Most write operations return tasks that can be waited for
2. **Type Safety**: Full typing with mypy strict mode enabled
3. **Error Hierarchy**: Custom exceptions in `meilisearch/errors.py`
4. **HTTP Abstraction**: Centralized HTTP handling with automatic retries and error conversion
5. **Model Validation**: Pydantic models for request/response validation

### Testing Strategy
- **Integration Tests**: Most tests run against real Meilisearch instance
- **Fixtures**: Automatic index cleanup between tests via `conftest.py`
- **Test Environment**: Uses `tests/common.py` for shared configuration
- **Coverage**: Tests cover client operations, index management, search, settings, and error handling

## 🔧 Development Guidelines

### Code Style
- **Black**: Line length 100, Python 3.8+ target
- **isort**: Black-compatible import sorting
- **mypy**: Strict type checking enabled
- **pylint**: Custom configuration in `pyproject.toml`

### Testing Requirements
- Must have running Meilisearch server on `http://127.0.0.1:7700` with master key `masterKey`
- Tests automatically clean up indexes after each run
- Use `pytest` for all test execution
- Coverage reports required for new features

### Error Handling
- All API errors convert to `MeilisearchApiError` with structured error information
- HTTP errors handled in `_httprequests.py`
- Timeout and communication errors have specific exception types

### Type Hints
- All public methods must have complete type annotations
- Use `from __future__ import annotations` for forward references
- Models use Pydantic for runtime validation

## 📦 SDK Architecture

### Client Hierarchy
```
Client (meilisearch/client.py)
├── Index management (create, list, delete indexes)
├── Global operations (health, version, stats, keys, tasks)
├── Multi-search functionality
└── Index (meilisearch/index.py)
    ├── Document operations (add, update, delete, get)
    ├── Search operations (search, facet_search)
    ├── Settings management (all index configuration)
    └── Task operations (wait_for_task, get_tasks)
```

### Models Structure
- **`models/document.py`**: Document and search result models
- **`models/index.py`**: Index settings and statistics models  
- **`models/key.py`**: API key management models
- **`models/task.py`**: Task status and batch operation models
- **`models/embedders.py`**: AI embedder configuration models

### HTTP Layer
- `_httprequests.py` handles all HTTP communication
- Automatic JSON serialization/deserialization
- Custom serializer support for complex types (datetime, UUID)
- Centralized error handling and retry logic

## 🧪 Test Organization

### Test Structure
```
tests/
├── client/          # Client-level operations
├── index/           # Index-specific operations  
├── settings/        # Index settings tests
├── models/          # Model validation tests
├── errors/          # Error handling tests
└── conftest.py      # Shared fixtures and cleanup
```

### Key Test Patterns
- Each test module focuses on specific functionality
- Tests use real Meilisearch server for integration testing
- Automatic cleanup ensures test isolation
- Tests verify both success and error cases

## 🔍 Common Development Tasks

### Adding New API Endpoints
1. Add method to appropriate class (`Client` for global, `Index` for index-specific)
2. Add type hints for parameters and return values
3. Add corresponding model classes if needed
4. Write integration tests covering success and error cases
5. Update documentation if it's a public feature

### Running Single Test Categories
```bash
# Test specific functionality
pipenv run pytest tests/client/          # Client operations
pipenv run pytest tests/index/           # Index operations  
pipenv run pytest tests/settings/        # Settings management
pipenv run pytest tests/models/          # Model validation
```

### Debugging
```python
import pdb
pdb.set_trace()  # Add breakpoint for debugging
```

## 📝 Release Process

Version management:
- Version defined in `meilisearch/version.py`
- Semantic versioning (MAJOR.MINOR.PATCH)
- Automated via GitHub Actions workflow
- Publishes to PyPI automatically on release