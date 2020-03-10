#!/bin/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
cd $HERE
PORT=${1:-"8890"}
MYHOST=${2:-"bin.bublina.eu.org"}
{
echo "Starting httpd at http://127.0.0.1:$PORT"
echo
echo "Example Caddy configuration:"
} 1>&2
cat <<EOF
$MYHOST {
  root /path/to/public
  proxy / http://127.0.0.1:$PORT {
    except /css /js /img /robots.txt /browserconfig.xml
    transparent
  }
  header /css Cache-Control "max-age=2592000"
  header /js Cache-Control "max-age=2592000"
  header /img Cache-Control "max-age=2592000"
  header /robots.txt Cache-Control "max-age=2592000"
  header /browserconfig.xml Cache-Control "max-age=2592000"
  gzip
}
EOF
#./genmin.sh
cd gen
./gen.sh
cd -
httpd -c $HERE/httpd.conf \
  -fvv -p 127.0.0.1:$PORT \
  -h $HERE/public

#  -u nobody
