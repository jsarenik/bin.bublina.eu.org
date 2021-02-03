#!/bin/sh
#
# crontab
# * * * * * /path/to/cleanup.sh

NOW=$(date +%s)
BINDIR=/tmp/bin
test -d $BINDIR || exit 1

# Delete pastes which are supposed to be deleted already
# Skip those which are meant to stay (those do not contain
# the env file in their directory OR have their EXP* values
# removed from that file)
/busybox/find $BINDIR -mindepth 2 -maxdepth 2 -type f -name env |
  while read i
  do
    PASTE=${i%/env}
    grep -q EXPIRED $i || continue && . $i
    echo $EXPIRED
    test $EXPIRED -le $NOW && rm -rf $PASTE
  done

# Delete the .limit records (empty files)
/busybox/find $BINDIR/.limit -type f -mmin +5 -delete
