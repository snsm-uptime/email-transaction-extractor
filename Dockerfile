ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /email_transaction_extractor

COPY pyproject.toml poetry.lock /email_transaction_extractor/

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /email_transaction_extractor

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "email_transaction_extractor.main:app", "--host", "0.0.0.0", "--port", "80"]

