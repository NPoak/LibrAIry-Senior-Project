# 1. Start with official Python 3.12 image (Debian Bookworm based)
FROM python:3.12-bookworm

# 2. Install System Deps & Node.js 20
# We use the official NodeSource setup script to get Node 20
RUN apt-get update && apt-get install -y curl build-essential git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 3. Install n8n globally via npm
RUN npm install -g n8n

# 4. Create the Virtual Environment for Python
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 5. Install your Python Libraries
# (Note: The versions you asked for are very high, ensure they exist on PyPI)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Create a user 'node' (n8n expects this user)
RUN useradd -m -d /home/node -s /bin/bash node

# 7. Setup permissions and switch user
WORKDIR /home/node
RUN chown -R node:node /home/node /opt/venv
USER node

# 8. Start n8n
ENTRYPOINT ["n8n"]
