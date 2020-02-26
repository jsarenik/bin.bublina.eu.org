#!/bin/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
cd $HERE
PORT=${1:-"8890"}
MYHOST=${2:-"clock.mysite.eu.org"}
{
echo "Starting httpd at http://127.0.0.1:$PORT"
echo
echo "Example Caddy configuration:"
} 1>&2
cat <<EOF
$MYHOST {
  proxy / http://127.0.0.1:$PORT {
    transparent
  }
  gzip
}
EOF
#./genmin.sh
httpd -c $HERE/httpd.conf \
  -fvv -p 127.0.0.1:$PORT \
  -h $HERE/public

#  -u nobody
