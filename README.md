# LibrAIry Senior Project

Welcome to the **LibrAIry Senior Project** repository! This project is an advanced, self-hosted AI automation system built on top of the [n8n Self-Hosted AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit). It is designed to run intelligent agents, process webhooks, and interact with large language models locally. **GitHub repository**: [https://github.com/NPoak/LibrAIry-Senior-Project.git](https://github.com/NPoak/LibrAIry-Senior-Project.git)

---

## 🏗️ System Architecture & Components

Our system is composed of several Dockerized services, orchestrated via `docker-compose.yml`:

- **n8n**: The core low-code automation engine used to build AI agents and process workflows. **All used n8n workflows is located in folder n8n/demo-data/workflows**.
- **Ollama**: A local LLM runner managing models like `llama3.2` and `gpt-oss:20b`.
- **Python Worker**: A custom FastAPI backend built from scratch (`/python-worker`) to handle custom logic and extended processing.
- **Qdrant**: A high-performance vector database used for Retrieval-Augmented Generation (RAG) and document search.(not use)
- **PostgreSQL**: The main relational database for storing n8n data.
- **Cloudflare Tunnel (`cloudflared`)**: Securely exposes our local n8n instance and webhooks to the public internet, bypassing complex firewall restrictions.
- **Portainer**: A management UI to monitor and manage Docker containers.

---

## 🏛️ University Server Configuration (Important)

**Note:** This repository is currently deployed on a **University Server**. Because of strict network rules and NAT, direct access to the services is a bit unique. 

Instead of accessing services directly via the server's public IP, we use two main methods:

1. **Cloudflare Tunnel**: n8n and its webhooks are exposed securely via a Cloudflare Tunnel URL (e.g., `https://n8n.librairy.work`). This means external integrations (like LINE messaging API) can reach our webhooks without needing a VPN.
2. **SSH Local Port Forwarding**: To access backend services (like the database or Ollama) from your local machine, you must use SSH tunneling. 

   **Example: Forwarding Ollama and PostgreSQL to your local machine**
   ```bash
   ssh -L 8888:127.0.0.1:11434 -L 5433:127.0.0.1:5432 llmadmin@10.13.229.6
   ```
   *After running this, you can access Ollama at `localhost:8888` and PostgreSQL at `localhost:5433` on your local machine.*

---

## 🚀 Getting Started

Follow these steps to initialize and start the environment.

### 1. Environment Setup
Copy the example environment file and fill in your secrets, passwords, and tokens.
```bash
cp .env.example .env
```

### 2. Running the System
We have provided convenient bash scripts in the `scripts/` directory to manage the lifecycle of the system.

- **Start the entire system (Nvidia GPU)**: 
  This will create the necessary Docker network (`librairy-net`) and bring up all services using your GPU.
  ```bash
  bash scripts/start.sh
  ```
- **Start the system (CPU Only)**:
  If you do not have an Nvidia GPU available, use this script instead.
  ```bash
  bash scripts/start-cpu.sh
  ```

### 3. Rapid Development & Deployment
If you are modifying the code inside the `n8n` or `python-worker` directories, you don't need to restart everything. Use the deployment script to rebuild and restart only those specific containers:
```bash
bash scripts/deploy-code.sh
```

### 4. Updating Services
To pull the latest base images and restart the services, run:
```bash
bash scripts/update-all.sh
```

---

## 🧪 Testing

The `/test_load` directory contains [k6](https://k6.io/) load testing scripts. These are crucial for ensuring our university server can handle the load when AI models are generating responses concurrently.

### Running a Test
You will need to have `k6` installed on your machine. 

For example, to run the LINE chatbot smoke test:
```bash
k6 run test_load/smoke-test-line.js
```

**Test Scripts include:**
- `smoke-test-line.js`: Sends a mock LINE webhook event to test the response of the n8n workflow and the AI models (set with a long timeout for 20B models).
- `test-web.js`, `test-web-edit.js`, etc.: Used for simulating web requests and form creations.

---

## 📜 License
This project is licensed under the Apache License 2.0.
