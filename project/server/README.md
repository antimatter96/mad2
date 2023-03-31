Make sure Python 3 is installed

Install all the requried dependecies

```bash
pip install -r requirements.txt
```

Migrate

```
flask db migrate
flask db upgrade
```

Run


python3.9 -m celery -A app.celery call application.background_workers.tasks.export_csv --kwargs='{"user_id": 1}'
