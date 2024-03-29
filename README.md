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
  -d 'username=testuser&password=password'
```

Access with the token.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTY3ODAzODYwN30.Hhc6uQir4CBANfWpv8zIohoOrzQzHPfh7tq8Y9nNyYUnwIkLhznCCpIX0dKpb8KG2GbDkobBqsbHPBHILYXPTh9Vbbrg8qTU_Amtmwq-nc4_USA6UYmZeqUyztVkB6EKZA8Mf-XmVQNKLASZT0XTyJfNlZOuoNgaJQglTuyDHK-xkFlIzsMtC9OJCO_StPM22P3u9e_GNG0j_0aVgQBYhQj4n97_pupfJuKmTUtrWZO7_PYeZJNDu5g6YfhdxKqrSBNWN0ig76onb_vi5w1k2TfZe26vvjX593Fh9QKSu_MTzjQVCfZTEX1edNlgxecJe0Wtl2b4kkE--g7_0l9_Jw'
```

Disable token.

```bash
  curl -X 'DELETE' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTY3ODAzODYwN30.Hhc6uQir4CBANfWpv8zIohoOrzQzHPfh7tq8Y9nNyYUnwIkLhznCCpIX0dKpb8KG2GbDkobBqsbHPBHILYXPTh9Vbbrg8qTU_Amtmwq-nc4_USA6UYmZeqUyztVkB6EKZA8Mf-XmVQNKLASZT0XTyJfNlZOuoNgaJQglTuyDHK-xkFlIzsMtC9OJCO_StPM22P3u9e_GNG0j_0aVgQBYhQj4n97_pupfJuKmTUtrWZO7_PYeZJNDu5g6YfhdxKqrSBNWN0ig76onb_vi5w1k2TfZe26vvjX593Fh9QKSu_MTzjQVCfZTEX1edNlgxecJe0Wtl2b4kkE--g7_0l9_Jw'
```

Register User.

```bash
curl -X 'POST' \
  http://127.0.0.1:8000/users \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"username": "test2", "email": "test@example.test", "full_name": "test second", "disabled": false, "password": "password"}'
```
