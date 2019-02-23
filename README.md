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

In a new Python ≥3.7 virtual environment containing this repo, run:

    $ cd ./irc-url-title-bot/
    $ pip install -Ur requirements.txt  # once
    $ python -m ircurltitlebot --config-path=/some/dir/config.json

Sample config JSON:
```json
{
  "host": "chat.freenode.net",
  "ssl_port": 6697,
  "nick": "Title[bot]",
  "nick_password": "",
  "channels": ["#some_chan1", "#some_chan2"],
  "ignores": ["some_user"]
}
```

It is recommended that the bot be auto-voiced in each channel.
