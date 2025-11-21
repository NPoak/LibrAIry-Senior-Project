# Start with the official n8n image
FROM n8nio/n8n:latest

# Switch to root user to install packages
USER root

# Install Python3 and PIP (if not already present or to ensure latest)
RUN apk add --update --no-cache python3 py3-pip

# Create a virtual environment (Recommended for modern Python/Alpine)
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the libraries you need
RUN pip install requirements.txt

# Switch back to the node user (required for n8n security)
USER node