# hbonds-web

[![build status](https://travis-ci.com/omwan/hbonds-web.svg?token=5xWekA9qZuZiHaZmy9Yj&branch=master)](https://travis-ci.com/omwan/hbonds-web)

Web server to generate scatter plots for SSI data from PDB

### Installation and Running Locally

Prerequisites:

* Python 3+
* pip
* PostgreSQL 11+

Steps:

1. Clone this repo
2. Install venv with `pip install virtualenv`
3. Create a virtual environment with ` virtualenv venv`
4. Run `source venv/bin/activate` to activate the newly created virtual environment
5. Install dependencies with `pip install -r requirements.txt`
6. Create a local PostgreSQL database and import the data, then create indexes from `ssi_indexes.sql` in the `sql` directory.
7. Set an environment variable DATABASE_URL with the database URL, eg: `postgres://<user>:<password>@localhost:5432/<database_name>`
8. To run locally, run `FLASK_APP=app.py FLASK_ENV=development python -m flask run`

If necessary, replace instances of `pip` with `pip3` or instances of `python` with `python3` to run with Python 3
