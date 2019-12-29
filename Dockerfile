FROM python:3.8-slim-buster
# python:3.7-slim-stretch (using Debian 9) has fewer issues with invalid SSL certificiates than python:3.7-slim-buster (using Debian 10).
# As of 2019-11-29, python:3.8-slim-stretch doesn't exist. See https://github.com/docker-library/python/issues/428
WORKDIR /app
COPY requirements.txt .
RUN sed -i 's/@SECLEVEL=2/@SECLEVEL=1/' /etc/ssl/openssl.cnf && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r ./requirements.txt
# Note: Regarding SECLEVEL, see https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=927461
# Lowering the SECLEVEL should allow more SSL certificates to be valid.
COPY ircurltitlebot ircurltitlebot
RUN groupadd -g 999 app && \
    useradd -r -m -u 999 -g app app
USER app
ENTRYPOINT ["python", "-m", "ircurltitlebot"]
CMD ["--config-path", "/config/config.yaml"]
STOPSIGNAL SIGINT
