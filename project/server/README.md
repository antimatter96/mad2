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
