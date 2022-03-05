# PWP SPRING 2022
# Guess The Location
## Group information
* Miko Palojärvi miko.palojarvi@student.oulu.fi
* Santeri Yritys santeri.yritys@student.oulu.fi
* Juho-Heikki Holmi juho-heikki.holmi@student.oulu.fi



# API Install instructions

0. Run all commands inside /api, unless told otherwise

1. Create and run Python virtual environment

      ```python -m venv .```


2. Install dependencies while inside the venv

    ```pip install -r requirements.txt```
  

3. Install PostgreSQL 14.1, set credentials as postgres:postgres

4. Create database named gtl_dev

5. Initiate the database with flask (in venv, inside gtl-folder)

    ```flask db init```

    ```flask db migrate```

    ```flask db upgrade```

6. Populate database with script (in venv, inside gtl-folder)
  
    ```python3 populate.py```

7. Get dump from db

      ```pg_dump gtl_dev > dbdump```
