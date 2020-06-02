FROM python:3

COPY dpm /workspace/dpm
COPY .secrets.baseline pyproject.toml /workspace/

WORKDIR /workspace

RUN pip install poetry
RUN poetry install
RUN poetry run tox
