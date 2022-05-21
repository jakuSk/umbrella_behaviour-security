import os
import sys
import requests
import time

from services.config_service import ConfigService


class UmbrellaReportingService:
    """Class to manage data from Umbrella reporting service"""

    def __init__(self, key: str, secret: str, config_service: ConfigService):
        self.__config = config_service
        self.__api_report_token = self.__get_token(key, secret, config_service)

    def __get_token(self, key, secret, config_service: ConfigService) -> str:
        """Method to get autorization token from auth api"""
        url = config_service.get_value('umbrella:urls:auth')
        headers = {'Accept': 'application/json'}

        token_request = requests.post(
            url, headers=headers, auth=requests.auth.HTTPBasicAuth(key, secret))

        token = token_request.json().get('access_token')

        if token is None:
            print("Auth_token not found. Exiting...")
            sys.exit(101)
        else:
            return(token)

    def __add_query_string(self, property_path: str) -> str:
        """Method to add query_parameters to url"""
        query_parameters = self.__config.get_value(property_path)
        query_string = '?'

        for key, value in query_parameters.items():
            query_string += f'{key}={value}&'

        return query_string[:-1]

    def get_identites(self) -> dict:
        """Method to get identities"""
        url = self.__config.get_value('umbrella:urls:identities')

        url = url.replace('{organization_id}', self.__config.get_value(
            property_path='umbrella:identities:organization_id'))

        url += self.__add_query_string('umbrella:identities:query_parameters')

        headers = {'Authorization': 'Bearer ' + self.__api_report_token,
                   'Accept': 'application/json'}

        response = requests.get(url, headers=headers).json()

        return_dict = {}

        for user in response['data']:
            return_dict[user['identity']['label']] = user['identity']['id']

        return return_dict

    def get_report_for_user(self, identity_id: str) -> dict:
        """Method to get report for user"""
        url = self.__config.get_value('umbrella:urls:reports')

        url = url.replace('{organization_id}', self.__config.get_value(
            property_path='umbrella:reports:organization_id'))

        url += self.__add_query_string('umbrella:reports:query_parameters')

        query_categories = self.__config.get_value(
            'umbrella:reports:query_categories')

        categories_string = ''
        for category in query_categories:
            categories_string += f'{category},'

        l = len(categories_string)
        query_categories = categories_string[:l-1]
        url += "&categories=" + query_categories

        url = url.replace('{query_categories}', query_categories)

        url += f"&identityids={identity_id}"

        headers = {'Authorization': 'Bearer ' + self.__api_report_token,
                   'Accept': 'application/json'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(
                f'Non 200 status code - {response.status_code} on dns report api.')
            print(response.json())
            sys.exit(102)

        return response.json()

    def process_dns_queries(self, report_data: dict, ) -> dict:
        """We have to parse domain, category and internal IP"""
        data_objects = report_data['data']
        return_dict = {}

        # Iterate through the dictionary of domains and check if the analyzed dns query fits our risk category
        for dns_log in data_objects:
            return_dict[dns_log['domain']] = None

        return return_dict

    def __is_id_on_list(self, id: int, list_to_search: list) -> bool:
        """Simple method to iterate through the list and find a matching ID. Here it is used to find if dns query fits our category"""
        for id_on_list in list_to_search:
            if id_on_list == id:
                return True

        return False

    def get_investigate_data(self, domain: str) -> dict:
        """Get data from Investigate API. Returns dict with risk_score value"""
        return_dict = {}
        return_dict['domain'] = domain
        api_token = os.environ['umb_investigate_token']
        url = self.__config.get_value('umbrella:urls:investigate') + domain
        api_headers = {}
        api_headers['Authorization'] = f'Bearer {api_token}'
        api_headers['Accept'] = 'application/json'

        response = requests.get(url, headers=api_headers, verify=True)
        if response.status_code != 200:
            print(
                f'Non 200 status code - {response.status_code} on investigate api.')
            print(response.json())
            sys.exit(1)

        # Here we add the risk_score for the domain into out return_dict
        return_dict['risk_score'] = response.json()['risk_score']

        return return_dict