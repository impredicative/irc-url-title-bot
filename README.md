# irc-url-title-bot
**irc-url-title-bot** is a Python 3.7 based IRC URL title posting bot.
It essentially posts the page titles of the URLs that are posted in the configured channels on an IRC server.
As a disclaimer, note that SSL verification is disabled, and that the posted titles are not guaranteed to be accurate
due to a number of factors.

## Links
* Code: https://github.com/impredicative/irc-url-title-bot
* Container: https://hub.docker.com/r/ascensive/irc-url-title-bot

## Examples
```text
<Adam> For image super-resolution, see https://arxiv.org/abs/1902.06068, and for more reviews see https://j.mp/ml-reviews.
<Title[bot]> ⤷ [1902.06068] Deep Learning for Image Super-resolution: A Survey | https://arxiv.org/pdf/1902.06068
<Title[bot]> ⤷ Review articles | freenode-machinelearning.github.io
<Eve> Thanks. Is github.com/visinf/n3net a good project? I've been studying bugs.python.org/file47781/Tutorial_EDIT.pdf
<Title[bot]> ⤷ GitHub - visinf/n3net: Neural Nearest Neighbors Networks (NIPS*2018)
<Title[bot]> ⤷ Python Tutorial
```
For more examples, see [`urltitle`](https://github.com/impredicative/urltitle/).

## Usage
The bot can work in multiple channels but on only one server.
To use with multiple servers, use an instance per server.

### Configuration
Prepare a private but version-controlled `config.yaml` file using the sample below.
```yaml
# Mandatory:
host: chat.freenode.net
ssl_port: 6697
nick: MyTitle[bot]
nick_password: the_correct_password
channels:
  - '#some_chan1'
  - '##some_chan2'

# Optional:
alerts_channel: '##mybot-alerts'
blacklist:
  title:
    - Invalid host
    - Untitled
  url:
    - model.fit
    - tf.app
ignores:
  - some_user1
  - some_user2
mode:

# Site-specific (optional):
sites:
  arxiv.org:
    format:
      - re:
          url: /pdf/(?P<url_id>.+?)(?:\.pdf)*$
        str:
          title: '{title} | https://arxiv.org/abs/{url_id}'
      - re:
          url: /abs/(?P<url_id>.+?)$
        str:
          title: '{title} | https://arxiv.org/pdf/{url_id}'
  bpaste.net:
    blacklist:
      title: show at bpaste
  imgur.com:
    blacklist:
      title: 'Imgur: The magic of the Internet'
```

#### Global settings

##### Mandatory
* **`host`**
* **`ssl_port`**
* **`nick`**
* **`nick_password`**
* **`channels`**

##### Optional
* **`alerts_channel`**: Some but not all warning and error alerts are sent to the this channel.
Its default value is `##{nick}-alerts`. The key `{nick}`, if present in the value, is formatted with the actual nick.
For example, if the nick is `MyTitle[bot]`, alerts will by default be sent to `##MyTitle[bot]-alerts`.
Since a channel name starts with #, the name if provided **must be quoted**.
It is recommended that the alerts channel be registered and monitored.
* **`blacklist/title`**: This is a list of strings. If a title is one of these strings, it is not posted.
The comparison is case insensitive.
* **`blacklist/url`**: This is a list of strings. If a URL is one of these strings, its title is not posted.
The comparison is case sensitive.
* **`ignores`**: This is a list of nicks to ignore.
* **`mode`**: This can for example be `+igR` for [Freenode](https://freenode.net/kb/answer/usermodes).
Setting it is recommended.

#### Site-specific settings
The site of a URL is as defined and returned by the
[`urltitle`](https://github.com/impredicative/urltitle/blob/master/urltitle/urltitle.py) package via its
`URLTitleReader().netloc(url)` method.

The following examples show various URLs and their corresponding sites:

| URL | Site |
| --- | ---- |
| https://www.google.com/search?q=asdf | google.com |
| https://google.com/search?q=hjkl | google.com |
| google.com/search?q=qwer | google.com |
| google.com | google.com |
| https://drive.google.com/drive/my-drive | drive.google.com |
| https://help.github.com/en/ | help.github.com |
| https://github.com/pytorch/pytorch | github.com
| https://www.amazon.com/gp/product/B01F8POA7U | amazon.com
| https://rise.cs.berkeley.edu/blog/ | rise.cs.berkeley.edu |
| https://www.swansonvitamins.com/web-specials | swansonvitamins.com |

Site-specific settings are specified under the top-level `sites` key.
The order of execution of the interacting operations is: `blacklist`, `format`.
Refer to the sample configuration for usage examples.

* **`blacklist/title`**: This is a single string.
If the title for a URL matching the site is this blacklisted string, the title is not posted.
The comparison is case sensitive.
* **`format`**: This contains a list of entries, each of which have keys `re/title` and/or `re/url` along with
`str/title`.
* **`format/re/title`**: This is a single regular expression pattern that is
[searched](https://docs.python.org/3/library/re.html#re.search) for in the title.
It is used to collect named [key-value pairs](https://docs.python.org/3/library/re.html#re.Match.groupdict) from the
match.
If there isn't a match, the next entry in the parent list, if any, is attempted.
* **`format/re/url`**: This is similar to `format/re/title`.
If both this and `format/re/url` are specified, both patterns must then match their respective strings, failing which
the next entry in the parent list, if any, is attempted.
* **`format/str/title`**: The key-value pairs collected using `format/re/title` and/or `format/re/url`,
are combined along with the default additions of both `title` and `url` as keys.
The key-value pairs are used to [format](https://docs.python.org/3/library/stdtypes.html#str.format_map) the provided
quoted title string. The default value is `{title}`.
If the title is thereby altered, any remaining entries in the parent list are skipped.

### Deployment
* As a reminder, it is recommended that the alerts channel be registered and monitored.
* It is recommended that the bot be auto-voiced (+V) in each channel.

* It is recommended that the bot be run as a Docker container using using Docker ≥18.09.2, possibly with
Docker Compose ≥1.24.0.
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
      - ./irc-url-title-bot:/config:ro
```
In the YAML, customize the relative path, e.g. `./irc-url-title-bot` of the volume source.
This should be the directory containing `config.yaml`.

From the directory containing the above YAML file, run `docker-compose up -d irc-url-title-bot`.
Use `docker logs -f irc-url-title-bot` to see and follow informational logs.

### Maintenance
If `config.yaml` is updated, the container must be restarted to use the updated file.
