#############
# Dependencies
#
#  This base stage just installs the dependencies required for production
#  without any development deps.
ARG PYTHON_VER=3.11
FROM python:${PYTHON_VER} AS base

# Allow for flexible Python versions, for broader testing
ARG PYTHON_VER=3.11
ENV PYTHON_VERSION=${PYTHON_VER}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -yqq && apt-get install -yqq shellcheck && apt-get clean

WORKDIR /usr/src/app

# Update pip to latest
RUN python -m pip install -U pip

# Install poetry for dep management
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.5
ENV PATH="$PATH:/root/.local/bin"
RUN poetry config virtualenvs.create false

# Bring in Poetry related files needed for other stages
COPY pyproject.toml poetry.lock ./

# Install only package Dependencies
RUN poetry install --only main

#########
# Linting
#
# Runs all necessary non Ansible linting and code checks
FROM base AS lint

# Install dev dependencies
RUN poetry install

# Copy in the application source and everything not explicitly banned by .dockerignore
COPY . .

RUN echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile .bandit.yml && \
    echo 'Running Pylint' && \
    pylint **/*.py

############
# Unit Tests
#
# This test stage runs true unit tests (no outside services) at build time, as
# well as enforcing codestyle and performing fast syntax checks. It is built
# into an image with docker-compose for running the full test suite.
FROM lint AS unittests

# Set a custom collection path for all ansible commands
# Note: This only allows for one path, not colon-separated, because we use it
# elsewhere
ARG ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
ENV ANSIBLE_COLLECTIONS_PATH=${ANSIBLE_COLLECTIONS_PATH}

ARG PYTHON_VER=3.11
ENV PYTHON_VERSION=${PYTHON_VER}

# Allows for custom command line arguments to be passed to ansible-test (like -vvv)
ARG ANSIBLE_SANITY_ARGS
ENV ANSIBLE_SANITY_ARGS=${ANSIBLE_SANITY_ARGS}
ARG ANSIBLE_UNIT_ARGS
ENV ANSIBLE_UNIT_ARGS=${ANSIBLE_UNIT_ARGS}

# For Module unit tests as we use some testing features avaiable in this collection
RUN ansible-galaxy collection install community.general

# Build Collection to run ansible-tests against
RUN ansible-galaxy collection build --output-path ./dist/ .

# Install built library
RUN ansible-galaxy collection install ./dist/networktocode*.tar.gz -p ${ANSIBLE_COLLECTIONS_PATH}

# Switch to the collection path for tests
WORKDIR ${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/networktocode/nautobot

# Run sanity tests
RUN echo 'Running Ansible Sanity Tests.' && \
    ansible-test sanity $ANSIBLE_SANITY_ARGS \
    --requirements \
    --python ${PYTHON_VER} \
    plugins/ && \
    echo 'Running Ansible Lint' && \
    ansible-lint

# Run unit tests
RUN ansible-test units $ANSIBLE_UNIT_ARGS --coverage --requirements --python ${PYTHON_VERSION}

############
# Integration Tests
FROM unittests AS integration

ARG ANSIBLE_INTEGRATION_ARGS
ENV ANSIBLE_INTEGRATION_ARGS=${ANSIBLE_INTEGRATION_ARGS}
ARG NAUTOBOT_VER
ENV NAUTOBOT_VER=${NAUTOBOT_VER}

# Integration test entrypoint
ENTRYPOINT ${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/networktocode/nautobot/tests/integration/entrypoint.sh

CMD ["--help"]
