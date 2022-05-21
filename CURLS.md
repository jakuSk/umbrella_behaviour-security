# curl preview

## Get token

API to get bearer token for reporting APIs

```bash
curl -i -u {key:secret} -X GET 'https://management.api.umbrella.com/auth/v2/oauth2/token' -H 'Accept: application/json'
```

```json
{
  "token_type": "bearer",
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2NTI5ODIwNjIsImlhdCI6MTY1Mjk3ODQ2MiwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTY1Mjk3ODQ2Miwic3ViIjoib3JnLzc5NjY1MTcvdXNlci8xMTg1Mjk1OSIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.CK2NWmfLbLvWHuedgLgd0IdWkPoPAWSEi-DDJuEllc7hM3Tj05RdKPB9anYH6w-zW0PdTIca8kLP8rAsG71GwxGB_ALFH-BR6G7olNofZJvEvfSw0y0Fcvwd02VB2ZjviFwv6BGNegxVJy7IBveSV3SlwQ8GjYTY5WgBB8RA1ukv6IN3gFEGQJgWZ5yWunWhlszEM0p8u8zcQR7c5f7CPdM_J5FSFs_SrEcOroJejyZKzbJs0EXPktWz9QOVMoJxKfBYN8X-8-4zEM50qSrnSt7X7Y-g7viiqzYnd0-BnJb0_zWwdl1sRNtsNqtiMuw1iOVMtF9JMakd-02yFRYBFg",
  "expires_in": 3600
}
```

## Top identities

API to get top identities

```bash
curl -i -X GET 'https://reports.api.umbrella.com/v2/organizations/7966517/top-identities?from=-7days&to=now&limit=100&offset=0' -H 'Accept: application/json' -H 'Authorization: Bearer {token}'
```

```json
{
  "meta": {},
  "data": [
    {
      "requests": 2274,
      "bandwidth": 170051,
      "identity": {
        "id": 585728824,
        "type": {
          "id": 34,
          "type": "anyconnect",
          "label": "Anyconnect Roaming Client"
        },
        "label": "VM_WIN11",
        "deleted": false
      },
      "counts": {
        "requests": 2274,
        "allowedrequests": 2273,
        "blockedrequests": 1
      },
      "rank": 1
    },
    {
      "requests": 660,
      "bandwidth": 280377304,
      "identity": {
        "id": 586214883,
        "type": {
          "id": 34,
          "type": "anyconnect",
          "label": "Anyconnect Roaming Client"
        },
        "label": "ASUS-1",
        "deleted": false
      },
      "counts": {
        "requests": 660,
        "allowedrequests": 659,
        "blockedrequests": 1
      },
      "rank": 2
    },
    {
      "requests": 201,
      "bandwidth": null,
      "identity": {
        "id": 586216275,
        "type": {
          "id": 34,
          "type": "anyconnect",
          "label": "Anyconnect Roaming Client"
        },
        "label": "Asus-2",
        "deleted": false
      },
      "counts": {
        "requests": 201,
        "allowedrequests": 201,
        "blockedrequests": 0
      },
      "rank": 3
    }
  ]
}
```

## dns activity
