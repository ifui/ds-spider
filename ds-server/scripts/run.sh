#!/bin/sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cd /root/ds-server || exit

if [ ! -f "./db.sqlite3" ]; then
  python manage.py migrate
fi

uwsgi uwsgi.ini

/bin/bash