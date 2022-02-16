# pylint: disable=invalid-name

import re

from meilisearch.version import __version__, qualified_version


def test_get_version():
    assert re.match(r'^(\d+\.)?(\d+\.)?(\*|\d+)$', __version__)

def test_get_qualified_version():
    assert qualified_version() == f"Meilisearch Python (v{__version__})"
