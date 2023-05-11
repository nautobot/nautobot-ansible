ARG NAUTOBOT_VER
ARG PYTHON_VER

FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VER}-py${PYTHON_VER} as nautobot

RUN pip install nautobot-bgp-models
COPY ./development/nautobot_config.py /opt/nautobot/nautobot_config.py
