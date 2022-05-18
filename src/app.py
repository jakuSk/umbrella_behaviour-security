
#!/usr/bin/env python3
import os
import sys

from services.umbrella_reporting_service import UmbrellaReportingService
from services.config_service import ConfigService

def main():
    config_service = ConfigService(config_name='config.json')
    key, secret = get_secrets('umb_reporting_key', 'umb_reporting_secret')


def get_secrets(key, secret) -> (str, str):
    try:
        key = os.environ[key]
        secret = os.environ[secret]
        return key, secret
    except KeyError as e:
        print("Environment variable {} not found... Exiting".format(e))
        sys.exit(1)
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit(100)

if __name__ == '__main__':
    main()