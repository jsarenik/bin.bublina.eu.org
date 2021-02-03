#!/bin/sh

# crontab
# */5 * * * * /path/to/cleanup.sh
NOW=$(date +%s)
BINDIR=/tmp/bin

test -d $DIR || exit 1
/busybox/find $BINDIR -mindepth 1 -maxdepth 1 -type d -name "[0-9a-f]*" |
  while read i
  do
    grep -q EXPIRED $i/env || continue && . $i/env
    echo $EXPIRED
    test $EXPIRED -le $NOW && rm -rf $i
  done

/busybox/find $BINDIR/.limit -type f -mmin +5 -delete
