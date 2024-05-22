# Welltory Task

This is a task for Welltory. Feel free to modify and extend the provided scripts as needed for your task requirements.

## Startup Instructions:

1. Create temporary PostgreSQL database (skip if you already have
   one):
   
   `docker run --rm -p 5432:5432 -d -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=welltory_task --name welltory_task_postgres postgres`
2. Create .env file: `cp .env.example .env`
3. Fill in .env file with your database connection details (skip if you created the database using the command in
   step 1).
4. Create virtual environment: `python -m venv venv`
5. Install dependencies:

```
source venv/bin/activate # Activate virtual environment
pip install -r requirements.txt
```

6. Create tables: `python db.py`
7. Create test data: `python factories.py`
8. Run main script to view results: `python main.py`
9. Delete test database: ` docker stop welltory_task_postgres`