# hbonds-web

![build status](https://travis-ci.com/omwan/hbonds-web.svg?token=5xWekA9qZuZiHaZmy9Yj&branch=master)

Web server to generate scatter plots for SSI data from PDB

### Installation and Running Locally

Prerequisites:

* Python 3+
* pip

Steps:

1. Install venv with `pip install virtualenv`
2. Clone this repo
3. Create a virtual environment with ` virtualenv venv`
4. Run `source venv/bin/activate` to activate the newly created virtual environment
5. Install dependencies with `pip install -r requirements.txt`
6. To run locally, run `FLASK_APP=app.py FLASK_ENV=development python -m flask run`

If necessary, replace instances of `pip` with `pip3` or instances of `python` with `python3` to run with Python 3