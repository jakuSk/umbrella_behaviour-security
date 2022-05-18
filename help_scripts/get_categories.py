#!/usr/bin/env python3

import requests

url = "https://reports.api.umbrella.com/v2/organizations/7966517/categories"
payload = None
headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2NTI4MTk5MTUsImlhdCI6MTY1MjgxNjMxNSwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTY1MjgxNjMxNSwic3ViIjoib3JnLzc5NjY1MTcvdXNlci8xMTg1Mjk1OSIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.ZBI3IBxrJiuV6EnoVeyFPlWSr5gKJAUCxOH_qh5lWZv7r9Sfq180slNxVYnK6FVfoxvoSE3ssZY7Wos3McXVVLNrUDxl51qb-0r9chT7Z0JMee2P_F4Yr9kMsSIfAEKYfROaroD6aFdK1ORlnbSIvXkmce9VAB_PoAmCVULukGNMQUKH94v_8qO1RCqbAPjG9OOxpGAWzVTfmInz122UxHqeXHV86BBPCqVn47f5_dVNZXr4eY63IsXvWApj1Fz5MAfRRB0Oa02AXlPs9cbikqOSi0nZOH-Jw3EzY6MJWAuDpF1RVv9nUUnhEIOdT3MsHqNdJP6FWq61eO60Lrk71w",
           "Accept": "application/json"}
response = requests.request('GET', url, headers=headers, data=payload)

json_response = response.json()

for category in json_response['data']:
    if category['type'] == 'security':
        print(f"{category['id']} - {category['label']}")