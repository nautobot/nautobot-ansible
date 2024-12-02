ARG NAUTOBOT_VER
ARG PYTHON_VER

FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VER}-py${PYTHON_VER} as nautobot

# Copy in the requirements file
COPY ./development/requirements.txt /opt/nautobot/requirements.txt

# Install the requirements
RUN pip install -r /opt/nautobot/requirements.txt

# Copy in the jobs
COPY ./development/jobs /opt/nautobot/jobs

# Copy in the development configuration file
COPY ./development/nautobot_config.py /opt/nautobot/nautobot_config.py
