
FROM n8nio/n8n:latest

# Install python3 
USER root

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# RUN apk add --update python3 py3-pip

USER node
RUN python3 -m pip install --user --break-system-packages pipx

# Add the path of the pipx installaion to PATH
ENV PATH="/home/node/.local/bin:$PATH" 