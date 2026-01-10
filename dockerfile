
# FROM n8nio/n8n:latest
FROM n8nio/n8n:1.123.10

# Install python3 
USER root

# 1. check OS while Build (for debug)
RUN cat /etc/os-release

RUN apk add --no-cache python3 py3-pip
# RUN apk add --update python3 py3-pip

USER node
RUN python3 -m pip install --user --break-system-packages pipx

# Add the path of the pipx installaion to PATH
ENV PATH="/home/node/.local/bin:$PATH" 
