### Install instructions

1. Create and run Python virtual environment

      ```python -m venv .```



2. Install dependencies inside environment
  pip install Flask
  pip install flask-sqlalchemy
  pip install psycopg2-binary
  pip install flask-migrate


3. Install PostgreSQL 14.1, credentials postgres:postgres

4. Create database gtl_dev

4. Initiate db with flask (inside src-folder)

    ```flask db init```
    ```flask db migrate```
    ```flask db upgrade```

5. Populate database with script 
  how
  to
  populate

99. Get dump from db

      ```pg_dump gtl_dev > dbdump```