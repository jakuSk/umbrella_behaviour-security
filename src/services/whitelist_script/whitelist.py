#!/usr/bin/env python3
import getopt
from getopt import GetoptError
import sys
import os
from curses import meta
import sqlalchemy as db
import sqlalchemy.exc as exc

from config_service import ConfigService

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"h:u:",["username="])
    except getopt.GetoptError:
        print('whitelist.py -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('whitelist.py -u <username>')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg

    config_service = ConfigService('config.json')
    db_user = config_service.get_value('database:user')
    connection_string = config_service.get_value(
        'database:connection_string')

    connection_string = connection_string.replace('{db_user}', db_user)
    connection_string = connection_string.replace(
        '{db_pass}', os.environ['db_pass'])

    try:
        engine = db.create_engine(connection_string)
        connection = engine.connect()
        metadata = db.MetaData()
        users_table = db.Table('users_identity', metadata, autoload=True, autoload_with=engine)
    except exc.NoSuchTableError as e:
        print(f'No such table: {e}')
        sys.exit(2)
    except exc.OperationalError as e:
        print(f'Couldn\'t connect to database. Please check config file')
        sys.exit(3)

    user_label_query = f"""SELECT rc.username, ui.umbrella_label
FROM radcheck rc
JOIN users_identity ui
ON ui.radcheck_id = rc.id
WHERE rc.username = '{username}';
"""

    user_label_query_result = connection.execute(user_label_query).fetchall()
    try:
        umbrella_label = user_label_query_result[0]['umbrella_label']
    except IndexError:
        print('User not found')
        sys.exit(2)

    user_whitelist_query = f"""UPDATE users_identity ui
SET whitelisted_from = CURRENT_DATE
WHERE ui.umbrella_label = '{umbrella_label}';"""

    connection.execute(user_whitelist_query)

    print(f'User {username} whitelisted')

if __name__ == "__main__":
   main(sys.argv[1:])