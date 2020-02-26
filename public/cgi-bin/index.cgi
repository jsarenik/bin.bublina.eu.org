#!/busybox/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
#export PATH=/busybox

WHERE=/tmp/bin
eval $(echo "$QUERY_STRING" | grep -o '[a-zA-Z][[:alnum:]]*=[-[:alnum:]/_+%]\+')

test "$REQUEST_METHOD" = "POST" -a -z "$pasteid" && {
echo "Content-Type: application/json; charset=UTF-8"
echo
#id=d0c8d91aa2b718dc
NOW=$(date +%s)
id=$(printf $(/busybox/dd if=/dev/random bs=4 count=2 2>/dev/null | /busybox/xxd -p))
dt=$(/busybox/dd if=/dev/random bs=2 count=16 2>/dev/null | /busybox/xxd -p | sed 's/\s\+$//' | tr -d '\n'; echo)
cat | jq -c "{status:0, id:\"$id\", url:\"\/?$id\", adata, ct, v:2, meta: {created: $NOW, time_to_live: 604800}, comments:[], comment_count:0, comment_offset:0, \"@context\":\"?jsonld=paste\", deletetoken:\"$dt\"}" > $WHERE/$id

cat <<EOF
{"status":0,"id":"$id","url":"\/?$id","deletetoken":"$dt"}
EOF
}

test "$REQUEST_METHOD" = "GET" -a -z "$pasteid" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  exec cat $HERE/a.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -n "$deletetoken" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  grep -Fwq "$deletetoken" $WHERE/$pasteid && { rm $WHERE/$pasteid; exec cat $HERE/b.html; } || exec cat $HERE/notdeleted.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -r $WHERE/$pasteid && {
  echo "Content-Type: application/jsan; charset=UTF-8"
  echo
  cat $WHERE/$pasteid
  jq .adata[3] $WHERE/$pasteid | grep -qFx 1 && rm $WHERE/$pasteid
}
