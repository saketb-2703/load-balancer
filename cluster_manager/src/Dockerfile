FROM python:3.8-slim

ARG ENV_CLI
ENV NODE=$ENV_CLI

COPY . /app

WORKDIR /app

ENTRYPOINT ["python3", "src/node.py"]
