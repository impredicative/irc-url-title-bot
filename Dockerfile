FROM python:3.7
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY ircurltitlebot ircurltitlebot
VOLUME /config
ENTRYPOINT ["python", "-m", "ircurltitlebot"]
CMD ["--config-path", "/config/config.json"]
