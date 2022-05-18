# umbrella_behaviour-security

1. [Requirements](#requirements)
1. [Steps - Score calculation](#steps---score-calculation)
    1. [Load configuration file](#load-configuration-file)
    1. [Load information for VPN users](#load-configuration-file)
    1. [Load data from Cisco Umbrella for VPN Users](#load-configuration-file)
    1. [Calculate risk score](#calculate-risk-score)
    1. [Save result into database](#save-result-into-database)

## Requirements

## Steps - Score calculation

### Load configuration file

### Load information for VPN users

### Load data from Cisco Umbrella for VPN Users

1. Get access token
1. Fetch access data

### Calculate risk score

### Save result into database

If user isn't on whitelist, save result

## Steps - Whitelisting script

### Usage

`./whitelist.py --user <username>`

### Description

If a user is misbehaving, we can add him to whitelist. Default expiration is 30 days.