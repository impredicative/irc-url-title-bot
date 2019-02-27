# irc-url-title-bot
**irc-url-title-bot** is a Python-based IRC URL title bot.
It essentially posts the page titles of the URLs that are posted in the configured channels on an IRC server.
As a disclaimer, note that SSL verification is disabled, and that the posted titles are not guaranteed to be accurate
due to a number of factors.

## Links
* Code: https://github.com/impredicative/irc-url-title-bot
* Container: https://hub.docker.com/r/ascensive/irc-url-title-bot

## Examples
```text
<Adam> For image super-resolution, see https://arxiv.org/abs/1902.06068, and for more reviews see https://j.mp/ml-reviews.
<Title[bot]> ⤷ [1902.06068] Deep Learning for Image Super-resolution: A Survey
<Title[bot]> ⤷ Review articles | freenode-machinelearning.github.io
<Eve> Thanks. Is github.com/visinf/n3net a good project? I've been studying bugs.python.org/file47781/Tutorial_EDIT.pdf
<Title[bot]> ⤷ GitHub - visinf/n3net: Neural Nearest Neighbors Networks (NIPS*2018)
<Title[bot]> ⤷ Python Tutorial
```
For more examples, see [`urltitle`](https://github.com/impredicative/urltitle/).
## Usage
The bot can work in multiple channels but on only one server.
To use with multiple servers, use an instance per server.

* Prepare a private but version-controlled `config.json` file using the sample below. All keys are mandatory.
```json
{
  "host": "chat.freenode.net",
  "ssl_port": 6697,
  "nick": "Title[bot]",
  "nick_password": "the_correct_password",
  "channels": ["#some_chan1", "#some_chan2"],
  "ignores": ["some_user"]
}
```

* Some but not all warning and error alerts are sent to `##{nick}-alerts`.
For example, if the nick is `Title[bot]`, these alerts will be sent to `##Title[bot]-alerts`.
It is recommended that the alerts channel be registered even if it is not monitored.

* It is recommended that the bot be auto-voiced (+V) in each channel.

* It is recommended that the bot be run as a Docker container using using Docker ≥18.09.2, possibly with
Docker Compose ≥1.24.0-rc1 or Kubernetes, etc.
To run the bot using Docker Compose, create or add to a version-controlled `docker-compose.yml` file:
```yaml
version: '3.7'
services:
  irc-url-title-bot:
    container_name: irc-url-title-bot
    image: ascensive/irc-url-title-bot:latest
    restart: always
    logging:
      options:
        max-size: 10m
        max-file: "3"
    volumes:
      - ./irc-url-title-bot/prod:/config:ro
```
In the YAML, customize the relative path, e.g. `./irc-url-title-bot/prod` to the volume source.
This should be the directory containing `config.json`.

From the directory containing the above YAML file, run `docker-compose up -d`.

If the configuration is updated, the bot must be restarted to use the updated configuration.
