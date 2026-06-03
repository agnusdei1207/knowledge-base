FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    "mcp>=1.27,<2" \
    "starlette>=0.37,<1" \
    "uvicorn>=0.30,<1"

WORKDIR /workspace

CMD ["python", "/workspace/scripts/knowledgebase_mcp_server.py"]
