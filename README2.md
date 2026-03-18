Step 1: create .env.example in cloned folder
test
- cp .env.example .env
  Step 2: start compose
  docker compose --profile gpu-nvidia up -d --build
  For update image version
  docker compose build --pull

Additional:
To Access n8n workflow (no VPN needed) -> https://carola-suppositious-gloatingly.ngrok-free.dev/
For ngrok tunnel to n8n (old approach which local ngrok start up -> changed: attach in docker compose of server)
ngrok http --url=carola-suppositious-gloatingly.ngrok-free.dev 5678 (n8n port)

TO use ollama,postgres,qdrant etc. in local : forwarding local port to service running on server port
ssh -L 8888:127.0.0.1:11434 -L 5433:127.0.0.1:5432 llmadmin@10.13.229.6

To use postgres via local terminal (not recommend)
psql -h 127.0.0.1 -p 5433 -U admin -d librairy
