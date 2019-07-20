FROM python:3.6

# Install pipenv and dependencies
WORKDIR /workdir
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

# Copy startup script
ARG WAIT_FOR_SCRIPT
ARG STARTUP_SCRIPT
COPY $WAIT_FOR_SCRIPT /usr/local/bin
COPY $STARTUP_SCRIPT /usr/local/bin
