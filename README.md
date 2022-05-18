# umbrella_behaviour-security

1. [Requirements](#requirements)
1. [Steps - Score calculation](#steps---score-calculation)
    1. [Load configuration file](#load-configuration-file)
        1. [Load umbrella key and secret stored in sysenv](#load-umbrella-key-and-secret-stored-in-sysenv)
    1. [Load information for VPN users](#load-configuration-file)
    1. [Load data from Cisco Umbrella for VPN Users](#load-configuration-file)
    1. [Calculate risk score](#calculate-risk-score)
    1. [Save result into database](#save-result-into-database)

## Requirements

## Steps - Score calculation

### Load configuration file

#### Load umbrella key and secret stored in sysenv

Secrets are named by default as `umb_reporting_key` and `umb_reporting_secret`.

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

| id | label |
|-----|-----|
|65|Command and Control|
|62|Mobile Threats|
|110|DNS Tunneling VPN|
|60|Drive-by Downloads/Exploits|
|106|Unauthorized IP Tunnel Access|
|108|Newly Seen Domains|
|109|Potentially Harmful|
|150|Cryptomining|
|61|Dynamic DNS|
|64|Command and Control|
|66|Malware|
|68|Phishing|
|67|Malware|
|63|High Risk Sites and Locations|

### Calculate risk score

### Save result into database

If user isn't on whitelist, save result

## Steps - Whitelisting script

### Usage

`./whitelist.py --user <username>`

### Description

If a user is misbehaving, we can add him to whitelist. Default expiration is 30 days.


## Exit codes

| exit code | reason |
|:-|-|
|100| unknown exceptions|
|101| failed to obtain bearer token|
|102| Non 2XX status code on API call|