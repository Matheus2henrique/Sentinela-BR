FROM python:3.12-slim
ENV SENTINELA_BASE=/home/claude TZ=America/Sao_Paulo SENTINELA_NODE_MODULES=/home/claude/node_modules
WORKDIR /home/claude
COPY real ./real
COPY sentinela_br ./sentinela_br
COPY package.json ./
RUN pip install --no-cache-dir -r sentinela_br/atualizacao/requirements.txt && apt-get update && apt-get install -y cron nodejs npm && npm install --no-audit --no-fund && rm -rf /var/lib/apt/lists/* \
 && crontab sentinela_br/atualizacao/crontab.txt
CMD ["cron", "-f"]
