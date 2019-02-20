# irc-url-title-bot
**irc-url-title-bot** is an IRC URL title bot.
It essentially posts the page titles of the URLs that are posted in the configured channels on an IRC server.

## Usage

Python ≥3.7 is required.

    $ cd ./irc-url-title-bot/
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
