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
NOW=$(date +%s)
test -n "$HTTP_X_REAL_IP" || HTTP_X_REAL_IP=$REMOTE_ADDR
LIMIT=$WHERE/limit/$(echo $HTTP_X_REAL_IP | tr -d '.:[]')
test -r $LIMIT && {
  LAST=$(stat -c "%Y" $LIMIT)
  test $((NOW-LAST)) -le 10 && {
    echo "{\"status\":1,\"message\":\"Please wait 10 seconds between each post.\"}"
    exit 1
  }
} || test -d $WHERE/limit || mkdir $WHERE/limit
touch $LIMIT
#id=d0c8d91aa2b718dc
dt=$(genrandom 4)
TMP=$(mktemp)
MAXSIZE=1m
head -c $MAXSIZE | grep -o '[^,]\+:[^:]\+[,}]' | sed 's/^{//;s/}$//' > $TMP
head -c 1 | grep -q . && {
    echo "{\"status\":1,\"message\":\"Maximum file size is $MAXSIZE.\"}"
    rm $TMP
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
  test -r $TD/next && next=$(cat $TD/next) || next=1
  test -d $ND || mkdir $ND
  mv $TMP $ND/$next
  echo $((next+1)) > $TD/next
  rmdir $ND/.lock
  echo "{\"status\":0,\"id\":\"$pasteid\",\"url\":\"/?$pasteid\"}"
else
  while
    id=$(genrandom)
    ! mkdir -p $WHERE/$id
  do : ; done
  TD=$WHERE/$id
  mv $TMP $TD/data
  {
  echo CREATED=$NOW
  echo DT=$dt
  } > $TD/env
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
  EXPIRE=$(grep -o '"expire":"[^"]\+"' $TD/data | tr -d '"' | cut -b8-11)
  tneve=0
  t5min=300
  t10mi=600
  t1hou=3600
  t1wee=604800
  t1mon=2592000
  t1yea=31536000
  eval EXPIRE=$(echo \$t$EXPIRE)
  TTL=$((CREATED+EXPIRE-NOW))
  # Following line is not needed because TTL will be negative
  # when EXPIRE is 0
  #test $EXPIRE -eq 0 && TTL=0
  DATA=$(grep -v '^"meta":' $TD/data | tr -d '\n')
  echo "\
{\
\"status\":0,\
\"id\":\"$pasteid\",\
\"url\":\"/?$pasteid\",\
$DATA,\
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


  echo $DATA | grep -oqF '0,1]' && rm -rf $TD
  exit
}

echo "Content-Type: application/json; charset=UTF-8"
echo
exec cat $HERE/nonexistent.json
