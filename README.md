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
<Eve> scholar.google.com and semanticscholar.org list academic articles.
<Title[bot]> ⤷ Google Scholar
<Title[bot]> ⤷ Semantic Scholar - An academic search engine for scientific articles
```
For more examples, see [`urltitle`](https://github.com/impredicative/urltitle/).
## Usage
The bot can work in multiple channels but on only one server.
To use with multiple servers, use an instance per server.

* Prepare a `config.json` file using the sample below. All keys are mandatory.
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
* It is recommended that the bot be auto-voiced (+V) in each channel.

* To run the bot as a Docker container, change to the directory containing the configured `config.json` file, and run:
```bash
docker run -d -v "$PWD":/config:ro ascensive/irc-url-title-bot
```
To auto-restart the container when the host restarts, include the `--restart always` option in the command above.
To view and follow the logs, use `docker logs`.
To rerun the newly created container in the future, refer to the container by its assigned name.
