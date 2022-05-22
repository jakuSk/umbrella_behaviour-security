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
    umbrella_service = UmbrellaReportingService(config_service)

    # Application logic
    # First get active identities from umbrella top-identities API
    identities_dict = umbrella_service.get_identites()
    # Then we get the mapping table from db that maps umbrella_label with username
    users = db_service.get_users_identities(identities_dict)

    # Then we get the reports for each user
    for users_index in range(len(users)):
        process_users_activity(umbrella_service, users,
                               users_index, db_service)

    t2 = time.perf_counter()
    print(f'Time taken to process {len(users)} users is {t2-t1}')


def process_users_activity(umbrella_service, users, users_index, db_service) -> int:
    """Method to process users activity and save it to the database."""
    report_data = umbrella_service.get_report_for_user(
        users[users_index][2])
    # users tuple contains 0: username 1: label 3: identity_id 4: report_data
    users[users_index] = (
        users[users_index][0], users[users_index][1], users[users_index][2], report_data)
    domain_info = umbrella_service.process_dns_queries(
        report_data=users[users_index][3])

    domain_list = []
    for domain in domain_info:
        # Get data from investigate API for each domain and add it to the list for risk score calculation
        domain_list.append(umbrella_service.get_investigate_data(domain))

    risk_score = risk_score_calculation.calculate_risk_score(domain_list)
    db_service.update_users_group(users[users_index][0], risk_score)
    return risk_score


if __name__ == '__main__':
    main()