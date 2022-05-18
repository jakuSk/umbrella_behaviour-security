import requests
import sys

from services.config_service import ConfigService


class UmbrellaReportingService:
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

        if token == None:
            print("Auth_token not found. Exiting...")
            sys.exit(101)
        else:
            return(token)
