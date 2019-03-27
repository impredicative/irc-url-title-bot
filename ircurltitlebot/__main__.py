import argparse
import logging
import json
from pathlib import Path

from ruamel.yaml import YAML

from ircurltitlebot import Bot, config

log = logging.getLogger(__name__)


def main() -> None:
    # Read args
    parser = argparse.ArgumentParser(prog=config.PACKAGE_NAME, description="IRC URL title posting bot")
    parser.add_argument('--config-path', required=True, help='Configuration file path, e.g. /some/dir/config.yaml')
    instance_config_path = Path(parser.parse_args().config_path)

    # Read user config
    log.debug('Reading instance configuration file %s', instance_config_path)
    instance_config = YAML().load(instance_config_path)
    instance_config = json.loads(json.dumps(instance_config))  # Recursively use a dict as the data structure.

    # Log user config
    logged_instance_config = instance_config.copy()
    del logged_instance_config['nick_password']
    log.info('Read user configuration file "%s" having configuration: %s',
             instance_config_path, json.dumps(logged_instance_config))

    # Set alerts channel
    if 'alerts_channel' not in instance_config:
        instance_config['alerts_channel'] = config.ALERTS_CHANNEL_FORMAT_DEFAULT
    instance_config['alerts_channel'] = instance_config['alerts_channel'].format(nick=instance_config['nick'])
    if instance_config['alerts_channel'] not in instance_config['channels']:
        instance_config['channels'].append(instance_config['alerts_channel'])

    # Process user config
    instance_config['nick:casefold'] = instance_config['nick'].casefold()
    instance_config['channels:casefold'] = [channel.casefold() for channel in instance_config['channels']]
    instance_config['ignores:casefold'] = [ignore.casefold() for ignore in instance_config.get('ignores', [])]

    # Process blacklist
    blacklists = instance_config['blacklist'] = instance_config.get('blacklist', {})
    blacklists['title'] = set(blacklists.get('title', set()))
    blacklists['title'] = {entry.casefold() for entry in blacklists['title']}
    blacklists['url'] = set(blacklists.get('url', set()))

    config.INSTANCE = instance_config

    # Start bot
    Bot()


if __name__ == '__main__':
    main()
