import os
from curses import meta
from time import time
import sqlalchemy as db

from services.config_service import ConfigService

class DatabaseService:
    """Class to managa data from database"""
    def __init__(self, config_service: ConfigService):
        db_user = config_service.get_value('database:user')
        connection_string = config_service.get_value('database:connection_string')

        connection_string = connection_string.replace('{db_user}', db_user)
        connection_string = connection_string.replace('{db_pass}', os.environ['db_pass'])

        self.__engine = db.create_engine(connection_string)
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__users_table = db.Table('users_identity', self.__metadata, autoload=True, autoload_with=self.__engine)
        self.__radcheck = db.Table('radcheck', self.__metadata, autoload=True, autoload_with=self.__engine)
        self.__radgroupreply = db.Table('radgroupreply', self.__metadata, autoload=True, autoload_with=self.__engine)

    def get_users_identities(self) -> list:
        """Method to get users identities"""
        query = '''SELECT rc.username, ui.umbrella_label FROM radcheck rc JOIN users_identity ui ON ui.radcheck_id = rc.id;'''

        users_query_result = self.__connection.execute(query).fetchall()
        
        return_list = []

        for user in users_query_result:
            return_list.append((user['username'], user['umbrella_label']))

        return return_list