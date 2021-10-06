FROM python:3.8-buster


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /BibleWay-BaptistChurch

COPY Pipfile Pipfile.lock /BibleWay-BaptistChurch/

# Install all packages & dependencies from Pipfile
RUN pip install pipenv
RUN pipenv install --dev --system --deploy


# Copy all files in local root directory to root of docker image
COPY . /BibleWay-BaptistChurch/