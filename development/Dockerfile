ARG NAUTOBOT_VER

# TODO: Switch back to the production (non-dev) Nautobot image when 3.0 is released
# FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VER} as nautobot
FROM ghcr.io/nautobot/nautobot-dev:${NAUTOBOT_VER} as nautobot

# Copy in the requirements file
COPY --chown=nautobot:nautobot ./development/requirements.txt /opt/nautobot/requirements.txt

# Install the requirements
RUN pip install -r /opt/nautobot/requirements.txt --no-deps

# Copy in the jobs
COPY --chown=nautobot:nautobot ./development/jobs /opt/nautobot/jobs

# Copy in the development configuration file
COPY --chown=nautobot:nautobot ./development/nautobot_config.py /opt/nautobot/nautobot_config.py
