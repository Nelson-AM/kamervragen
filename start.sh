#!/bin/bash

source /opt/bin/activate

cd /opt/tkv/

service elasticsearch restart
service redis-server restart

sleep 20

supervisord -n -c conf/supervisor.conf
