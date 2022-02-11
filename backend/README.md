### Install instructions

0. Run all commands inside /backend, unless told otherwise

1. Create and run Python virtual environment

      ```python -m venv .```


2. Install dependencies while inside the venv

    ```pip install Flask flask-sqlalchemy psycopg2-binary flask-migrate```
  

3. Install PostgreSQL 14.1, set credentials as postgres:postgres

4. Create database named gtl_dev

5. Initiate the database with flask (in venv, inside src-folder)

    ```flask db init```

    ```flask db migrate```

    ```flask db upgrade```

6. Populate database with script (in venv, inside src-folder)
  
    ```python3 populate.py```

7. Get dump from db

      ```pg_dump gtl_dev > dbdump```

