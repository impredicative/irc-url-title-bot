#!/usr/bin/env bash
docker run --name irc-url-title-bot --restart always -v /home/devuser/PycharmProjects/freenode-bots/irc-url-title-bot/dev:/config:ro ascensive/irc-url-title-bot