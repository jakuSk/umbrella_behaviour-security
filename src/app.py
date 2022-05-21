#!/usr/bin/env python3
import os
import sys
import time
import risk_score_calculation

from services.umbrella_reporting_service import UmbrellaReportingService
from services.config_service import ConfigService
from services.database_service import DatabaseService


def main():
    """Main method of the application."""
    # Service creation
    t1 = time.perf_counter()
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
    for x in range(len(users)):
        report_data = umbrella_service.get_report_for_user(users[x][2])
        users[x] = (users[x][0], users[x][1], users[x][2], report_data)
        domain_info = umbrella_service.process_dns_queries(report_data=users[x][3])

        domain_list = []
        for domain in domain_info:
            domain_list.append(umbrella_service.get_investigate_data(domain))
        
        risk_score = risk_score_calculation.calculate_risk_score(domain_list)
        db_service.update_users_group(users[x][0], risk_score)

    t2 = time.perf_counter()
    print(f'Time taken to process {len(users)} users is {t2-t1}')

def get_secrets(key, secret) -> (str, str):
    """Method to get the secrets from the environment variables."""
    try:
        key = os.environ[key]
        secret = os.environ[secret]
        return key, secret
    except KeyError as error:
        print(f'Environment variable {error} not found... Exiting')
        sys.exit(1)
    except Exception as error:
        print(f'Error: {error}')
        sys.exit(100)


if __name__ == '__main__':
    main()