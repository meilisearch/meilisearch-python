FROM python:3.8.4-buster

COPY Pipfile .
COPY Pipfile.lock .

RUN apt-get update -y

# Install pipenv and compilation dependencies
RUN pip3 install pipenv
RUN pipenv install --dev
