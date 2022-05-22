# umbrella_behaviour-security

- [umbrella_behaviour-security](#umbrella_behaviour-security)
  - [Requirements](#requirements)
    - [Python packages (pip)](#python-packages-pip)
    - [Software](#software)
  - [Steps - Score calculation](#steps---score-calculation)
    - [Load configuration file](#load-configuration-file)
      - [Secrets](#secrets)
      - [Load umbrella key and secret stored in sysenv](#load-umbrella-key-and-secret-stored-in-sysenv)
    - [Load information for VPN users](#load-information-for-vpn-users)
    - [Load data from Cisco Umbrella for VPN Users](#load-data-from-cisco-umbrella-for-vpn-users)
      - [Security categories](#security-categories)
    - [Calculate risk score](#calculate-risk-score)
    - [Save result into database](#save-result-into-database)
  - [Steps - Whitelisting script](#steps---whitelisting-script)
    - [Usage](#usage)
    - [Description](#description)
  - [Exit codes](#exit-codes)
  - [TODOs:](#todos)

## Requirements

### Python packages (pip)

Install pip requirements file `pip install -r src/requirements.txt`

1. psycopg2 - PostgreSQL driver
1. sqlalchemy - Database toolkit for python

### Software

1. PostgreSQL

This application has been teseted with PostgreSQL 12.

Table users_identity must be created.
```sql
CREATE TABLE public.users_identity
(
    id serial NOT NULL,
    radcheck_id integer NOT NULL,
    umbrella_label character varying(32) NOT NULL,
    whitelist_from date,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.users_identity
    OWNER to radius;

ALTER TABLE IF EXISTS public.users_identity
    ADD CONSTRAINT radcheck_id FOREIGN KEY (radcheck_id)
    REFERENCES public.radcheck (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;
```

## Steps - Score calculation

### Load configuration file

#### Secrets

1. `umb_reporting_key` - Generated key for umbrella reporting
1. `umb_reporting_secret` - Generated secret for umbrella reporting
1. `db_pass` - Database password

#### Load umbrella key and secret stored in sysenv

Method get_secrets to get secrets for cisco Umbrella
```python
def get_secrets(key, secret) -> (str, str):
    try:
        key = os.environ[key]
        secret = os.environ[secret]

        return key, secret
    except Exception as e:
        print("Error: {}".format(e))
```

### Load information for VPN users

### Load data from Cisco Umbrella for VPN Users

1. Get access token
1. Fetch access data - Queried by security categories

#### Security categories

Security categories can be obtained from `help_script/get_categories.py`

| id  | label                         |
| --- | ----------------------------- |
| 65  | Command and Control           |
| 62  | Mobile Threats                |
| 110 | DNS Tunneling VPN             |
| 60  | Drive-by Downloads/Exploits   |
| 106 | Unauthorized IP Tunnel Access |
| 108 | Newly Seen Domains            |
| 109 | Potentially Harmful           |
| 150 | Cryptomining                  |
| 61  | Dynamic DNS                   |
| 64  | Command and Control           |
| 66  | Malware                       |
| 68  | Phishing                      |
| 67  | Malware                       |
| 63  | High Risk Sites and Locations |

### Calculate risk score

### Save result into database

If user isn't on whitelist, save result

## Steps - Whitelisting script

### Usage

`./whitelist.py -u <username>`

### Description

If a user is misbehaving, we can add him to whitelist. Default expiration is 30 days.


## Exit codes

| exit code | reason                          |
| :-------- | ------------------------------- |
| 100       | unknown exceptions              |
| 101       | failed to obtain bearer token   |
| 102       | Non 2XX status code on API call |



## TODOs:
1. add [radius ddl](https://wiki.freeradius.org/config/PostgreSQL-DDL-script) to docs