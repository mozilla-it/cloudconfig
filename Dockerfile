FROM python:3

COPY dpm /workspace/dpm
COPY .coveragerc .secrets.baseline pyproject.toml /workspace/

WORKDIR /workspace

RUN pip install .
RUN pip install tox
RUN tox
##RUN poetry config virtualenvs.create false
#RUN poetry install --no-ansi
#RUN poetry run tox
