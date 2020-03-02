#!/busybox/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
export PATH=/busybox:$PATH

WHERE=/tmp/bin
eval $(echo "$QUERY_STRING" | grep -o '[a-zA-Z][[:alnum:]]*=[-[:alnum:]/_+%]\+')

genrandom(){
  BYTES=${1:-1}
  dd if=/dev/random bs=8 count=$BYTES 2>/dev/null \
    | od -A n -t x1 \
    | tr -d ' \n'
}

test "$REQUEST_METHOD" = "POST" -a -z "$pasteid" && {
echo "Content-Type: application/json; charset=UTF-8"
echo
#id=d0c8d91aa2b718dc
NOW=$(date +%s)
id=$(genrandom)
mkdir -p $WHERE/$id || id=$(genrandom)
dt=$(genrandom 4)
{
echo CREATED=$NOW
echo DT=$dt
} > $WHERE/$id/env
grep -o '[^,]\+:[^:]\+[,}]' | sed 's/^{//;s/}$//' > $WHERE/$id/data

echo "{\"status\":0,\"id\":\"$id\",\"url\":\"/?$id\",\"deletetoken\":\"$dt\"}"
exit
}

test "$REQUEST_METHOD" = "GET" -a -z "$pasteid" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  exec cat $HERE/a.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -n "$deletetoken" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  . $WHERE/$pasteid/env
  test "$deletetoken" = "$DT" \
    && { rm -rf $WHERE/$pasteid; exec cat $HERE/b.html; } \
    || exec cat $HERE/notdeleted.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -r $WHERE/$pasteid/data && {
  echo "Content-Type: application/json; charset=UTF-8"
  echo
  NOW=$(date +%s)
  . $WHERE/$pasteid/env
  TTL=$((CREATED+604800-NOW))
  DATA=$(grep -v '^"meta":' $WHERE/$pasteid/data | tr -d '\n')
  echo "\
{\
\"status\":0,\
\"id\":\"$pasteid\",\
\"url\":\"/?$pasteid\",\
$DATA,\
\"meta\":{\"created\":$CREATED,\"time_to_live\":$TTL},\
\"comments\":[],\
\"comment_count\":0,\
\"comment_offset\":0,\
\"@context\":\"?jsonld=paste\"\
}"

  echo $DATA | grep -oq '0,1]' && rm -rf $WHERE/$pasteid
  exit
}

echo "Content-Type: application/json; charset=UTF-8"
echo
exec cat $HERE/nonexistent.json
