import sys
import requests

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

        print(key)
        print(secret)
        print(url)
        print(token_request)
        print(token_request.status_code)

        token = token_request.json().get('access_token')

        if token is None:
            print("Auth_token not found. Exiting...")
            sys.exit(101)
        else:
            return(token)

    def get_report_for_user(self, user: str) -> dict:
        """Method to get report for user"""
        url = self.__config.get_value('umbrella:urls:reports')
        url += self.__config.get_value('umbrella:reports:report_query')

        url = url.replace('{organization_id}', self.__config.get_value(
            property_path='umbrella:reports:organization_id'))
        query_categories = self.__config.get_value(
            'umbrella:reports:query_categories')

        categories_string = ''
        for category in query_categories:
            categories_string += f'{category},'

        l = len(categories_string)
        query_categories = categories_string[:l-1]

        url = url.replace('{query_categories}', query_categories)

        headers = {'Authorization': 'Bearer ' + self.__api_report_token,
                   'Accept': 'application/json'}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f'Non 200 status code - {response.status_code} on dns report api.')
            print(response.json())
            sys.exit(102)

        return response.json()