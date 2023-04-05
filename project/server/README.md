Make sure Python 3 is installed

Install all the requried dependecies

```bash
pip install -r requirements.txt
```

Migrate

```sh
flask db migrate
flask db upgrade
```


Open these in different shells [can run some in screen]
```sh
redis-server

./server.sh

./celery_periodic.sh
./celery_ondemand.sh
```

Specific Celery Task

```sh
python3.9 -m celery -A app.celery call application.background_workers.tasks.export_csv --kwargs='{"user_id": 1}'

python3.9 -m celery -A app.celery call application.background_workers.tasks.import_csv --kwargs='{"user_id": 12, "filename":"1_fab27440-bc18-4706-bc4d-5977ceeda8c4.csv"}'
```
