FROM google/cloud-sdk

RUN echo deb http://deb.debian.org/debian stable main >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y install python3 python3-pip pipenv unzip lftp libpq-dev && \
    apt-get clean

COPY dpm /workspace/dpm
COPY bin /workspace/bin
COPY .secrets.baseline Pipfile.lock Pipfile setup.py /workspace/

WORKDIR /workspace

#RUN pipenv install && \
#    pipenv run pip freeze | grep -v pkg-resources | sed -e 's|^-e ||g' -e 's|\(.*\)egg=\(.*\)|\2@\1egg=\2|g' > requirements.txt && \
#    pip3 install --upgrade --no-cache-dir .

RUN pip3 install --upgrade --no-cache-dir .

RUN pytest && \
    behave dpm/tests/bdd
