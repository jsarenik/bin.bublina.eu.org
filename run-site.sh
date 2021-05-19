#!/bin/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
cd $HERE
WHERE=/tmp/bin
PORT=${1:-"8890"}
MYHOST=${2:-"bin.bublina.eu.org"}
{
echo "Starting httpd at http://127.0.0.1:$PORT"
echo
echo "Example Caddy2 configuration:"
} 1>&2
cat <<EOF
$MYHOST {
  encode zstd gzip
  file_server {
    index index.html index.txt
  }
  @static {
    path /css/* /js/* /img/* /robots.txt /browserconfig.xml
  }
  handle @static {
    root * $PWD/public
    header Cache-Control "max-age=31536000"
  }
  handle /* {
    reverse_proxy /* http://127.0.0.1:$PORT {
      header_up X-Real-IP {remote_host}
    }
  }
}
EOF
#./genmin.sh
cd gen
./gen.sh
cd -
test -d $WHERE || mkdir -p $WHERE
# This is a hack to disable limit for local testing
rm -rf $WHERE/.limit; mkdir $WHERE/.limit
/busybox/httpd -c $HERE/httpd.conf \
  -fvv -p 127.0.0.1:$PORT \
  -h $HERE/public

#  -u nobody
