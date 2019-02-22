FROM python:3.7

COPY requirements.txt /app/
COPY ircurltitlebot /app/

WORKDIR /app
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "-m", "ircurltitlebot"]
