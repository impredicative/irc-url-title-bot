FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY ircurltitlebot ircurltitlebot
ENTRYPOINT ["python", "-m", "ircurltitlebot"]
CMD ["--config-path", "/config/config.json"]
