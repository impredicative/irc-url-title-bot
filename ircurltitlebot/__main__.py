import argparse
import logging
import json

from ircurltitlebot import Bot, config

config.configure_logging()

log = logging.getLogger(__name__)


def main() -> None:
    # Read args
    parser = argparse.ArgumentParser(prog=config.PACKAGE_NAME, description="IRC URL title bot")
    parser.add_argument('--config-path', required=True, help='Configuration file path, e.g. /some/dir/config.json')
    instance_config_path = parser.parse_args().config_path

    # Read user config
    log.debug('Reading instance configuration file %s', instance_config_path)
    with open(instance_config_path) as instance_config_file:
        instance_config = json.load(instance_config_file)
    logged_instance_config = instance_config.copy()
    del logged_instance_config['nick_password']
    log.info('Read user configuration file "%s" having configuration: %s',
             instance_config_path, json.dumps(logged_instance_config))
    config.INSTANCE = instance_config

    # Start bot
    Bot().serve()


if __name__ == '__main__':
    main()
