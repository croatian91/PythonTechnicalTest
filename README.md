# Origin Markets Backend Test

#### Project Quickstart

Inside a virtual environment running Python 3:

- `pip install -r requirements.txt`
- `./origin/manage.py migrate` to migrate.
- `./origin/manage.py loaddata users` to load users.
- `./origin/manage.py loaddata bonds` to load bonds.
- `./origin/manage.py runserver` to run server.
- `./origin/manage.py test bonds` to run tests.

#### ADMIN CREDENTIALS

- username: test
- password: test

#### API

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:

```
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
```

---

We should be able to send a request to:

`GET /bonds/`

to see something like:

```
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
```

We would also like to be able to add a filter such as:
`GET /bonds/?legal_name=BNPPARIBAS`

to reduce down the results.
