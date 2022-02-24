FROM python:3.9 as base

# Install python packages
WORKDIR /app/dataperf
COPY requirements.txt /app/dataperf/requirements.txt

ENV PIP_EXTRA_INDEX_URL=https://snapshots.linaro.org/ldcg/python-cache/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

# Install dataperf code
COPY . /app/dataperf

RUN chmod +x /app/dataperf/scripts/start.sh

ENTRYPOINT ["/app/dataperf/scripts/start.sh"]

