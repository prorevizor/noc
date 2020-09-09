# Base layer containing system packages and requirements
FROM python:3.8.5-slim-buster AS code
ENV\
    DJANGO_SETTINGS_MODULE=noc.settings \
    NOC_THREAD_STACK_SIZE=524288 \
    NOC_PYTHON_INTERPRETER=/usr/local/bin/python3 \
    PYTHONPATH=/opt/noc:/opt:/usr/local/bin/python3.8 \
    PROJ_DIR=/usr
# ADD thin.tgz /

COPY . /opt/noc/
WORKDIR /opt/noc/

RUN \
    apt update && apt-get install -y --no-install-recommends \
    build-essential \
    bzip2 \
    cmake \
    curl \
    gcc \
    libffi6 \
    libffi-dev \
    libjemalloc2 \
    libmemcached-dev \
    libmemcached11 \
    libpq-dev \
    libssl-dev \
    zlib1g-dev \
    && (./scripts/build/get-noc-requirements.py activator classifier cache-memcached cache-redis login-ldap login-pam login-radius prod-tools cython testing | pip3 install -r /dev/stdin )\
    && cythonize -i /opt/noc/speedup/*.pyx \
    && mkdir /opt/nocspeedup \
    && cp /opt/noc/speedup/*.so /opt/nocspeedup \
    && pip3 uninstall -y Cython \
    && apt remove gcc cmake build-essential -y \
    && rm -rf /var/lib/apt/lists/*

VOLUME /opt/noc
VOLUME /usr/local/lib/python3.8/site-packages/django

EXPOSE 1200

HEALTHCHECK --interval=10s --timeout=1s \
    CMD curl -f http://0.0.0.0:1200/health/ || exit 1

FROM code AS dev

RUN \
    apt update && apt-get install -y --no-install-recommends \
    snmp \
    vim \
    && (./scripts/build/get-noc-requirements.py dev | pip3 install -r /dev/stdin )\
    && rm -rf /var/lib/apt/lists/*

FROM nginx:alpine AS static

RUN apk add --no-cache curl

COPY --from=code /usr/local/lib/python3.8/site-packages/django /usr/lib/python3.8/site-packages/django
COPY --from=code /opt/noc/ui /opt/noc/ui
