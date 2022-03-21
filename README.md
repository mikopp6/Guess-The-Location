# PWP SPRING 2022

# Guess The Location

### Group information

- Miko Palojärvi miko.palojarvi@student.oulu.fi
- Santeri Yritys santeri.yritys@student.oulu.fi

## API Install instructions

0. Run all commands inside /api, unless told otherwise

1. Create and run Python virtual environment

   `python -m venv .`

2. Install dependencies while inside the venv

   `pip install -r requirements.txt`

3. Initiate the database with flask (in venv, inside gtl-folder)

   `flask init-db`

4. Populate database (in venv, inside gtl-folder)

   `flask testgen`

5. Start api (in venv, inside gtl-folder)

   `flask run`

## Additional stuff

### Documentation

The documentation can be found at:

/apidocs/


### Testing

Run tests (in venv, inside gtl-folder)

`pytest`

Test coverage:

`pytest --cov-report term-missing --cov=gtl tests/`

The errors that were found in testing consisted mainly of oversights in model attributes, e.g., missing unique values. Some http errors were also incorrect.


### Pylint

Run pylint (in venv)

`pylint .\gtl\ --rcfile=.\gtl\.pylintrc --output=pylint`