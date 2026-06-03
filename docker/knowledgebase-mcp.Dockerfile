FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    "mcp>=1.27.2,<2" \
    "starlette>=1.2.1,<2" \
    "uvicorn>=0.48.0,<1"

WORKDIR /workspace

CMD ["python", "/workspace/scripts/knowledgebase_mcp_server.py"]
