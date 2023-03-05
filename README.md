# API server for practice project for mantine table with next 13 app dir

<https://github.com/YasuhiroOsajima/mantine-table-app-dir>

Start server.

```bash
sh start.sh
```

Get new token.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=testuser&password=password&scope=&client_id=&client_secret=' # noqa: E501
```

Access with the token.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTY3ODAyMjk4MH0.3Lt49TGD0MxutGNcab-mzTSD6axi00bojPWrRF5fQvw'
```
