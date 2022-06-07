FROM python:3.8.4-buster

COPY Pipfile .
COPY Pipfile.lock .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc

# Install pipenv and compilation dependencies
RUN pip3 install pipenv
RUN pipenv install --dev
