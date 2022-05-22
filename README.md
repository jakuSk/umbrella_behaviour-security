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


__Freeradius_Postgres_DDLscript__
```sql
/*
 * $Id$
 *
 * Postgresql schema for FreeRADIUS
 *
 * All field lengths need checking as some are still suboptimal. -pnixon 2003-07-13
 *
 */

/*
 * Table structure for table 'radacct'
 *
 * Note: Column type bigserial does not exist prior to Postgres 7.2
 *       If you run an older version you need to change this to serial
 */
CREATE TABLE radacct (
	RadAcctId		bigserial PRIMARY KEY,
	AcctSessionId		text NOT NULL,
	AcctUniqueId		text NOT NULL UNIQUE,
	UserName		text,
	GroupName		text,
	Realm			text,
	NASIPAddress		inet NOT NULL,
	NASPortId		text,
	NASPortType		text,
	AcctStartTime		timestamp with time zone,
	AcctUpdateTime		timestamp with time zone,
	AcctStopTime		timestamp with time zone,
	AcctInterval		bigint,
	AcctSessionTime		bigint,
	AcctAuthentic		text,
	ConnectInfo_start	text,
	ConnectInfo_stop	text,
	AcctInputOctets		bigint,
	AcctOutputOctets	bigint,
	CalledStationId		text,
	CallingStationId	text,
	AcctTerminateCause	text,
	ServiceType		text,
	FramedProtocol		text,
	FramedIPAddress		inet,
	FramedIPv6Address	inet,
	FramedIPv6Prefix	inet,
	FramedInterfaceId	text,
	DelegatedIPv6Prefix	inet
);
-- This index may be useful..
-- CREATE UNIQUE INDEX radacct_whoson on radacct (AcctStartTime, nasipaddress);

-- For use by update-, stop- and simul_* queries
CREATE INDEX radacct_active_session_idx ON radacct (AcctUniqueId) WHERE AcctStopTime IS NULL;

-- Add if you you regularly have to replay packets
-- CREATE INDEX radacct_session_idx ON radacct (AcctUniqueId);

-- For use by onoff-
CREATE INDEX radacct_bulk_close ON radacct (NASIPAddress, AcctStartTime) WHERE AcctStopTime IS NULL;

-- For use by cleanup scripts
-- Works well for timeout queries, where ((acctstoptime IS NULL) AND (acctupdatetime < (now() - '1 day'::interval)))
-- as well as removing old sessions from the database.
--
-- Although at first glance it appears where an index on AcctUpdateTime with condition WHERE AcctStopTime IS NULL;
-- would be more effective, the query planner refused to use the index (for some unknown reason), and doing it this
-- way allows the index to be used for both timeouts and cleanup.
CREATE INDEX radacct_bulk_timeout ON radacct (AcctStopTime NULLS FIRST, AcctUpdateTime);

-- and for common statistic queries:
CREATE INDEX radacct_start_user_idx ON radacct (AcctStartTime, UserName);
-- and, optionally
-- CREATE INDEX radacct_stop_user_idx ON radacct (acctStopTime, UserName);

/*
 * Table structure for table 'radcheck'
 */
CREATE TABLE radcheck (
	id			serial PRIMARY KEY,
	UserName		text NOT NULL DEFAULT '',
	Attribute		text NOT NULL DEFAULT '',
	op			VARCHAR(2) NOT NULL DEFAULT '==',
	Value			text NOT NULL DEFAULT ''
);
create index radcheck_UserName on radcheck (UserName,Attribute);
/*
 * Use this index if you use case insensitive queries
 */
-- create index radcheck_UserName_lower on radcheck (lower(UserName),Attribute);

/*
 * Table structure for table 'radgroupcheck'
 */
CREATE TABLE radgroupcheck (
	id			serial PRIMARY KEY,
	GroupName		text NOT NULL DEFAULT '',
	Attribute		text NOT NULL DEFAULT '',
	op			VARCHAR(2) NOT NULL DEFAULT '==',
	Value			text NOT NULL DEFAULT ''
);
create index radgroupcheck_GroupName on radgroupcheck (GroupName,Attribute);

/*
 * Table structure for table 'radgroupreply'
 */
CREATE TABLE radgroupreply (
	id			serial PRIMARY KEY,
	GroupName		text NOT NULL DEFAULT '',
	Attribute		text NOT NULL DEFAULT '',
	op			VARCHAR(2) NOT NULL DEFAULT '=',
	Value			text NOT NULL DEFAULT ''
);
create index radgroupreply_GroupName on radgroupreply (GroupName,Attribute);

/*
 * Table structure for table 'radreply'
 */
CREATE TABLE radreply (
	id			serial PRIMARY KEY,
	UserName		text NOT NULL DEFAULT '',
	Attribute		text NOT NULL DEFAULT '',
	op			VARCHAR(2) NOT NULL DEFAULT '=',
	Value			text NOT NULL DEFAULT ''
);
create index radreply_UserName on radreply (UserName,Attribute);
/*
 * Use this index if you use case insensitive queries
 */
-- create index radreply_UserName_lower on radreply (lower(UserName),Attribute);

/*
 * Table structure for table 'radusergroup'
 */
CREATE TABLE radusergroup (
	id			serial PRIMARY KEY,
	UserName		text NOT NULL DEFAULT '',
	GroupName		text NOT NULL DEFAULT '',
	priority		integer NOT NULL DEFAULT 0
);
create index radusergroup_UserName on radusergroup (UserName);
/*
 * Use this index if you use case insensitive queries
 */
-- create index radusergroup_UserName_lower on radusergroup (lower(UserName));

--
-- Table structure for table 'radpostauth'
--

CREATE TABLE radpostauth (
	id			bigserial PRIMARY KEY,
	username		text NOT NULL,
	pass			text,
	reply			text,
	CalledStationId		text,
	CallingStationId	text,
	authdate		timestamp with time zone NOT NULL default now()
);

/*
 * Table structure for table 'nas'
 */
CREATE TABLE nas (
	id			serial PRIMARY KEY,
	nasname			text NOT NULL,
	shortname		text NOT NULL,
	type			text NOT NULL DEFAULT 'other',
	ports			integer,
	secret			text NOT NULL,
	server			text,
	community		text,
	description		text
);
create index nas_nasname on nas (nasname);
```


__Table users_identity must be created.__
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