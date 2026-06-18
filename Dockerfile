ARG PYTHON_VERSION=3.12
ARG PYTHON_VARIANT=bookworm
FROM python:${PYTHON_VERSION}-${PYTHON_VARIANT}

WORKDIR /app
COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -e .
CMD ["python", "-c", "from src.GraphTypeDefinitions.schema import schema; print(schema.as_str())"]
