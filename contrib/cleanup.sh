#!/bin/sh

# crontab
# */5 * * * * /path/to/cleanup.sh

DIR=/tmp/bin
test -d $DIR || exit 1
/busybox/find $DIR -mtime +7 -mindepth 1
