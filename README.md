[![Build
Status](https://travis-ci.org/dimagi/captain.svg?branch=master)](https://travis-ci.org/dimagi/captain)

<img src="https://raw.githubusercontent.com/dimagi/captain/master/apps/deploy/static/captain/img/captain.png" width="300"/>

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
