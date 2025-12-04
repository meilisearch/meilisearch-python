# Override parent conftest.py fixtures for auto-launch tests

import pytest


@pytest.fixture(scope="session")
def client():
    """Override client fixture to return None."""
    return None


@pytest.fixture(autouse=True)
def clear_indexes():
    """Override clear_indexes to do nothing."""
    yield


@pytest.fixture(autouse=True)
def clear_all_tasks():
    """Override clear_all_tasks to do nothing."""
    yield
