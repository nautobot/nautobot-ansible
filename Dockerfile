#############
# Dependencies
#
#  This base stage just installs the dependencies required for production
#  without any development deps.
ARG PYTHON_VER=3.8
FROM python:${PYTHON_VER} AS base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -yqq && apt-get install -yqq shellcheck && apt-get clean

WORKDIR /usr/src/app

# Update pip to latest
RUN python -m pip install -U pip

# Install poetry for dep management
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="$PATH:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# Install project manifest
COPY pyproject.toml .

# Install poetry.lock from which to build
COPY poetry.lock .

# Install all dependencies
RUN poetry install

# Allow for flexible Python versions, for broader testing
ARG PYTHON_VER
ENV PYTHON_VERSION=${PYTHON_VER}

# Set a custom collection path for all ansible commands
# Note: This only allows for one path, not colon-separated, because we use it
# elsewhere
ARG ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
ENV ANSIBLE_COLLECTIONS_PATH=${ANSIBLE_COLLECTIONS_PATH}

# For Module unit tests as we use some testing features avaiable in this collection
RUN ansible-galaxy collection install community.general

# Copy in the application source and everything not explicitly banned by
# .dockerignore
COPY . .

#########
# Linting
#
# Runs all necessary linting and code checks
FROM base AS lint


# We should look into pylint/flake8, etc. in the future
# RUN echo 'Running Flake8' && \
#     flake8 . && \
RUN echo 'Running Black' && \
    black --check --diff . && \
    # Removed and running Pylint in unit tests after project has been created
    # echo 'Running Pylint' && \
    # find . -name '*.py' | xargs pylint  && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile .bandit.yml


############
# Unit Tests
#
# This test stage runs true unit tests (no outside services) at build time, as
# well as enforcing codestyle and performing fast syntax checks. It is built
# into an image with docker-compose for running the full test suite.
FROM base AS unittests

ARG PYTHON_VER=3.8
ENV PYTHON_VERSION=${PYTHON_VER}

# Allows for custom command line arguments to be passed to ansible-test (like -vvv)
ARG ANSIBLE_SANITY_ARGS
ENV ANSIBLE_SANITY_ARGS=${ANSIBLE_SANITY_ARGS}
ARG ANSIBLE_UNIT_ARGS
ENV ANSIBLE_UNIT_ARGS=${ANSIBLE_UNIT_ARGS}

# Ansible sanity and unit tests
#
# Runs the sanity and unit tests inside the container build context to isolate
# thsoe tests from all runtime influences

# Build Collection to run ansible-tests against
RUN ansible-galaxy collection build --output-path ./dist/ .

# Install built library
RUN ansible-galaxy collection install ./dist/networktocode*.tar.gz

# Switch to the collection path for tests
WORKDIR ${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/networktocode/nautobot

# Run sanity tests
RUN ansible-test sanity $ANSIBLE_SANITY_ARGS \
    --requirements \
    --skip-test pep8 \
    --python ${PYTHON_VER} \
    plugins/

# Run unit tests
RUN ansible-test units $ANSIBLE_UNIT_ARGS --coverage --python $PYTHON_VERSION

############
# Integration Tests
FROM unittests AS integration

ARG ANSIBLE_INTEGRATION_ARGS
ENV ANSIBLE_INTEGRATION_ARGS=${ANSIBLE_INTEGRATION_ARGS}

# Integration test entrypoint
ENTRYPOINT ${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/networktocode/nautobot/tests/integration/entrypoint.sh

CMD ["--help"]
