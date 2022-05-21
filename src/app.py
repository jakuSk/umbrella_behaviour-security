#!/usr/bin/env python3
import os
import sys

from services.umbrella_reporting_service import UmbrellaReportingService
from services.config_service import ConfigService
from services.database_service import DatabaseService


def main():
    """Main method of the application."""
    # Service creation
    config_service = ConfigService(config_name='config.json')
    db_service = DatabaseService(config_service)
    key, secret = get_secrets('umb_reporting_key', 'umb_reporting_secret')
    umbrella_service = UmbrellaReportingService(key, secret, config_service)

    # Application logic
    # First get active identities from umbrella top-identities API
    identities_dict = umbrella_service.get_identites()
    # Then we get the mapping table from db that maps umbrella_label with username
    users = db_service.get_users_identities(identities_dict)

    # Then we get the reports for each user
    for identity in users:
        print(umbrella_service.get_report_for_user(identity[2]))


def get_secrets(key, secret) -> (str, str):
    """Method to get the secrets from the environment variables."""
    try:
        key = os.environ[key]
        secret = os.environ[secret]
        return key, secret
    except KeyError as error:
        print(f"Environment variable {error} not found... Exiting")
        sys.exit(1)
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(100)


if __name__ == '__main__':
    main()