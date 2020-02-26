#!/busybox/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
#export PATH=/busybox

eval $(echo "$QUERY_STRING" | grep -o '[a-zA-Z][[:alnum:]]*=[-[:alnum:]/_+%]\+')

test "$REQUEST_METHOD" = "POST" -a -z "$pasteid" && {
  cat > /tmp/test
echo "Content-Type: application/json; charset=UTF-8"
echo
# {"adata":[["MDXs5nNTWulZyfBT91e7nw==","Hd/0rqWAeIc=",100000,256,128,"aes","gcm","zlib"],"plaintext",0,0],"meta":{"expire":"1week"},"v":2,"ct":"g6pB6bj3n802qZxyoXreMNfkiZm3TyCSVfEPGz2zpCqaH4I="}
#id=d0c8d91aa2b718dc
id=$(printf $(/busybox/dd if=/dev/random bs=4 count=2 2>/dev/null | /busybox/xxd -p))
cat <<EOF
{"status":0,"id":"$id","url":"\\\/?$id","deletetoken":"e02f12fc179563ddfcc4ea795f2689776aa64dcab3c24d2df37ed156dfe59ef1"}
EOF
#{"status":0,"id":"$id","url":"\/?$id"}
#{"adata":[["AEcq3qqI6FfQ6iSaj+NV4A==","U7U8CvtWOIw=",100000,256,128,"aes","gcm","zlib"],"plaintext",0,1],"meta":{"expire":"1week"},"v":2,"ct":"TLCFCrcT95PdtFsk0olNbTDeueAmi3XpSgrtN9+1uRj8vQ=="}
#{"status":0,"id":"1109170743e45aa9","url":"\/?1109170743e45aa9","deletetoken":"1b42081cfce05988c1aa7163546d0e181aaeaa4cf4a5bde389c5b604c26d47c4"}
#{"status":0,"id":"1109170743e45aa9","url":"\/?1109170743e45aa9","adata":[["AEcq3qqI6FfQ6iSaj+NV4A==","U7U8CvtWOIw=",100000,256,128,"aes","gcm","zlib"],"plaintext",0,1],"v":2,"ct":"TLCFCrcT95PdtFsk0olNbTDeueAmi3XpSgrtN9+1uRj8vQ==","meta":{"created":1582741257,"time_to_live":604678},"comments":[],"comment_count":0,"comment_offset":0,"@context":"?jsonld=paste"}
#  echo "Content-Type: text/html; charset=UTF-8"
#  echo
#  exec cat $HERE/a.html
}

test "$REQUEST_METHOD" = "GET" -a -z "$pasteid" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  exec cat $HERE/a.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -n "$deletetoken" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  exec cat $HERE/b.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" && {
  echo "Content-Type: application/jsan; charset=UTF-8"
  echo
  pasteid=$(/busybox/httpd -d "$pasteid")
  cat /tmp/test | jq -c "{status:0, id:\"$pasteid\", url:\"\\\/?$pasteid\", adata, ct, v:2, meta: {created: 1582741257, time_to_live: 620000}, comments:[], comment_count:0, comment_offset:0, \"@context\":\"?jsonld=paste\"}"
#cat <<EOF
#{"status":0,"id":"$pasteid","url":"\/?$pasteid","adata":[["AEcq3qqI6FfQ6iSaj+NV4A==","U7U8CvtWOIw=",100000,256,128,"aes","gcm","zlib"],"plaintext",0,1],"v":2,"ct":"TLCFCrcT95PdtFsk0olNbTDeueAmi3XpSgrtN9+1uRj8vQ==","meta":{"created":1582741257,"time_to_live":604678},"comments":[],"comment_count":0,"comment_offset":0,"@context":"?jsonld=paste"}
#EOF
#cat /tmp/test
}

#echo "Content-Type: text/plain; charset=UTF-8"


#set
# Shell router
#case $REQUEST_URI in
#  /more/digital/*) . $HERE/digital.sh;;
#  /analog/*) . $HERE/analog.sh;;
#  /tools/timestamptodate/*) . $HERE/timestamptodate.sh;;
#esac
