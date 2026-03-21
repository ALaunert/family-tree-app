FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN python -c "import tomllib; from pathlib import Path; print('\n'.join(tomllib.loads(Path('/app/pyproject.toml').read_text())['project']['dependencies']))" > /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "-m", "http.server", "8000"]
