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
cat \
  | jq -c "{status:0, id:\"$id\", url:\"\/?$id\", adata, ct, v:2, meta: {created: $NOW, time_to_live: 604800}, comments:[], comment_count:0, comment_offset:0, \"@context\":\"?jsonld=paste\"}" \
  > $WHERE/$id/data
echo "$dt" > $WHERE/$id/dt

cat <<EOF
{"status":0,"id":"$id","url":"\/?$id","deletetoken":"$dt"}
EOF
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
  grep -Fxq $deletetoken $WHERE/$pasteid/dt && { rm -rf $WHERE/$pasteid; exec cat $HERE/b.html; } || exec cat $HERE/notdeleted.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -r $WHERE/$pasteid/data && {
  echo "Content-Type: application/jsan; charset=UTF-8"
  echo
  cat $WHERE/$pasteid/data
  jq .adata[3] $WHERE/$pasteid/data | grep -qFx 1 && rm -rf $WHERE/$pasteid
  exit
}

echo "Content-Type: application/json; charset=UTF-8"
echo
cat <<EOF
{"status":1,"message":"Paste does not exist, has expired or has been deleted."}
EOF
