# Captain

## Setup

Captain is a Django app that deploys commcare-hq. It uses sqlite3 as its database and redis for running its asynchronous task queue, `rq`.

```
pip install -r requirements.txt
touch captain.db
./manage.py migrate
./manage.py runserver
```

## Deploying Captain

To update captain, run `fab deploy` from your terminal
