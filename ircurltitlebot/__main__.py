import argparse
import logging
import json
import sys

from . import Bot, config

config.configure_logging()

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(prog=config.PACKAGE_NAME, description="IRC URL title bot")
    parser.add_argument('--config-path', required=True, help='Configuration file path, e.g. /some/dir/config.json')
    user_config_path = parser.parse_args().config_path

    log.debug('Reading user configuration file %s', user_config_path)
    with open(user_config_path) as user_config_file:
        user_config = json.load(user_config_file)
    log.info('Read user configuration file "%s" having configuration: %s',
             user_config_path, json.dumps(user_config).replace(user_config['nick_password'], '<password>'))

    try:
        log.debug('Initializing bot.')
        Bot(user_config).start()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()
