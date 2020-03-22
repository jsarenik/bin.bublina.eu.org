#!/busybox/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
export PATH=/busybox:$PATH

WHERE=/tmp/bin
test "$QUERY_STRING" = "" \
  || eval $(echo "$QUERY_STRING" | grep -o '[a-zA-Z]\+=[[:alnum:]]\+')

# Use just first letter of HTTP_ACCEPT - either 'a' or 't'
#  HTTP_ACCEPT='text/html...
#  HTTP_ACCEPT='application/javascript...
HTA="$(echo $HTTP_ACCEPT | head -c1)$REQUEST_METHOD"
O=""
test "$pasteid" = "" || {
  test -r $WHERE/$pasteid/data && { O=p; test "$deletetoken" = "" || O=d; }
}

# DEBUG
#echo $HTTP_ACCEPT 1>&2
#echo $HERE/${HTA}${O}.sh 1>&2
. $HERE/${HTA}${O}.sh
