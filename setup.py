from setuptools import setup, find_packages
from meilisearch.version import __version__

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "requests"
    ],
    name="meilisearch",
    version=__version__,
    author="Charlotte Vermandel",
    author_email="charlotte@meilisearch.com",
    description="The python client for Meilisearch API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meilisearch/meilisearch-python",
    packages=find_packages(exclude=("tests*",)),
    project_urls={"Documentation": "https://docs.meilisearch.com/",},
    keywords="search python meilisearch",
    platform="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data = {
        "meilisearch": ["py.typed"],
    },
    include_package_data=True,
    python_requires=">=3",
)
