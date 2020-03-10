#!/busybox/sh

a="/$0"; a=${a%/*}; a=${a:-.}; a=${a#/}/; HERE=$(cd $a; pwd)
export PATH=/busybox:$PATH

WHERE=/tmp/bin
test "$QUERY_STRING" = "" \
  || {
    eval $(echo "$QUERY_STRING" | grep -o '[a-zA-Z]\+=[[:alnum:]]\+')
    test "$pasteid" = "" || {
      test -r $WHERE/$pasteid/data && { O=p; test "$deletetoken" = "" || O=d; }
    }
  }
}
TMP=$(mktemp)
MAXSIZE=1m
head -c $MAXSIZE | grep -o '[^,]\+:[^:]\+[,}]' \
  | sed 's/^{//;s/}$//' \
  | tee $TMP-meta \
  | grep -v '^"meta":' \
  > $TMP
head -c 1 | grep -q . && {
    echo "{\"status\":1,\"message\":\"Maximum file size is $MAXSIZE.\"}"
    rm -rf $TMP*
    exit 1
}
if
  P=$(grep '^"pasteid":' $TMP)
then
  P=${P##*:\"}
  pasteid=${P%\",}
  TD=$WHERE/$pasteid
  ND=$TD/comment
  while ! mkdir -p $ND/.lock; do sleep 0.1; done
  next=$(cat $TD/next) || { next=1; mkdir $ND; }
  mv $TMP $ND/$next
  rm -rf $TMP*
  echo $((next+1)) > $TD/next
  rmdir $ND/.lock
  echo "{\"status\":0,\"id\":\"$pasteid\",\"url\":\"/?$pasteid\"}"
else
  while
    #id=d0c8d91aa2b718dc
    id=$(genrandom)
    ! mkdir -p $WHERE/$id
  do : ; done
  TD=$WHERE/$id
  mv $TMP $TD/data
  EXPIRE=$(grep -o '"expire":"[^"]\+"' $TMP-meta | cut -b11-14)
  rm -rf $TMP*
  tneve=0
  t5min=300
  t10mi=600
  t1hou=3600
  t1wee=604800
  t1mon=2592000
  t1yea=31536000
  eval EXPIRES=$(echo \$t$EXPIRE)
  {
  echo CREATED=$NOW
  echo EXPIRES=$EXPIRES
  test "$EXPIRES" = "0" || echo EXPIRED=$((NOW+EXPIRES))
  } > $TD/env
  #dt=34e75668370b52182e2b4549ad8305a9dcb8d65ec3b9b39d84b63b200cbb14d7
  dt=$(genrandom 32)
  echo DT=$dt > $TD/dt
  echo "{\"status\":0,\"id\":\"$id\",\"url\":\"/?$id\",\"deletetoken\":\"$dt\"}"
fi

exit
}

test "$REQUEST_METHOD" = "GET" -a -z "$pasteid" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  echo "<!DOCTYPE html>"
  eval $(echo "$HTTP_COOKIE" | grep -o '[a-zA-Z][[:alnum:]]*=[[:alnum:]]\+')
  test -n "$lang" && lang=" lang=\"$lang\""
  echo "<html$lang>"
  exec cat $HERE/a.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -n "$deletetoken" && {
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  echo "<!DOCTYPE html>"
  eval $(echo "$HTTP_COOKIE" | grep -o '[a-zA-Z][[:alnum:]]*=[[:alnum:]]\+')
  test -n "$lang" && lang=" lang=\"$lang\""
  echo "<html$lang>"
  TD=$WHERE/$pasteid
  . $TD/env
  . $TD/dt
  test "$deletetoken" = "$DT" \
    && { rm -rf $TD; exec cat $HERE/b.html; } \
    || exec cat $HERE/notdeleted.html
}

test "$REQUEST_METHOD" = "GET" -a -n "$pasteid" -a -r $WHERE/$pasteid/data && {
  echo "Content-Type: application/json; charset=UTF-8"
  echo
  NOW=$(date +%s)
  TD=$WHERE/$pasteid
  . $TD/env
  TTL=$((CREATED+EXPIRES-NOW))
  # Following line is not needed because TTL will be negative
  # when EXPIRES is 0
  #test $EXPIRES -eq 0 && TTL=0
  echo "\
{\
\"status\":0,\
\"id\":\"$pasteid\",\
\"url\":\"/?$pasteid\",\
$(cat $TD/data),\
\"meta\":{\"created\":$CREATED,\"time_to_live\":$TTL},"

if
  ! test -d $TD/comment
then
  echo "\
\"comments\":[],\
\"comment_count\":0,\
\"comment_offset\":0,\
\"@context\":\"?jsonld=paste\"\
}"
else
NUM=$(cat $TD/next)
NUM=$((NUM-1))
echo "\
\"comment_count\":$NUM,\
\"comment_offset\":0,\
\"@context\":\"?jsonld=paste\",\
\"comments\":["
for i in $(seq $NUM)
do
  CREATED=$(stat -c "%Y" $TD/comment/$i)
  ID=$(md5sum $TD/comment/$i | cut -b-16)
  test $i -eq 1 && echo "{" || echo ",{"
  cat $TD/comment/$i
  echo ",\"meta\":{\"created\":$CREATED,\"icon\":\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAIAAAC0tAIdAAAABnRSTlMAAAAAAABupgeRAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAQ0lEQVQokWNkgAGHBQkMuMGBhAUMDAxMeFRgAlqqZsQUQvYAxLkUm01+mBxIWIDmBnJcwoJVFJeraBom+IMCDdAy5gEFVRIcKzO8OgAAAABJRU5ErkJggg==\"},\"id\":\"$ID\""
  echo "}"
done
echo "]}"
fi

# Use just first letter of HTTP_ACCEPT - either 'a' or 't'
#  HTTP_ACCEPT='text/html...
#  HTTP_ACCEPT='application/javascript...

. $HERE/${HTTP_ACCEPT%${HTTP_ACCEPT#?}}${REQUEST_METHOD}${O}.sh
