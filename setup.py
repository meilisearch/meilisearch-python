from setuptools import find_packages, setup

from meilisearch.version import __version__

setup(
    packages=find_packages(exclude=("tests*",)),
    include_package_data=True,
    package_data={"meilisearch": ["py.typed"]},
)
