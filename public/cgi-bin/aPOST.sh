#!/busybox/sh

genrandom(){
  BYTES=${1:-8}
  head -c $BYTES /dev/random \
    | od -A n -t x1 \
    | tr -d ' \n'
}

echo "Content-Type: application/json; charset=UTF-8"
echo
NOW=$(date +%s)
HTTP_X_REAL_IP=${HTTP_X_REAL_IP:-"$REMOTE_ADDR"}
# Limit number of seconds from last POST attempt
LIMITS=10
LIMIT=$WHERE/.limit/$(echo $HTTP_X_REAL_IP | tr -d '.:[]')
LAST=$(stat -c "%Y" $LIMIT 2>/dev/null || echo 999; touch $LIMIT) && {
  test $((NOW-LAST)) -le $LIMITS && {
    echo "{\"status\":1,\"message\":\"Please wait $LIMITS seconds between \
each post. Counter is reset on every retry.\"}"
    exit 1
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
  ID=$(md5sum $TMP | cut -b-16)
  mv $TMP $ND/$ID
  echo ",\"meta\":{\"created\":$NOW,\"icon\":\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAIAAAC0tAIdAAAABnRSTlMAAAAAAABupgeRAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAQ0lEQVQokWNkgAGHBQkMuMGBhAUMDAxMeFRgAlqqZsQUQvYAxLkUm01+mBxIWIDmBnJcwoJVFJeraBom+IMCDdAy5gEFVRIcKzO8OgAAAABJRU5ErkJggg==\"},\"id\":\"$ID\"" \
    >> $ND/$ID
  rmdir $ND/.lock
  rm -rf $TMP*
  echo "{\"status\":0,\"id\":\"$pasteid\",\"url\":\"/?$pasteid\"}"
else
  while
    #id=d0c8d91aa2b718dc
    id=$(genrandom)
    ! mkdir -p $WHERE/$id
  do : ; done
  TD=$WHERE/$id

  # Following time definitions may be kept in sync with
  # the configuration according to which the index.html
  # is generated, in that case sending a hand-crafted
  # JSON will not help and the paste will be deleted
  #
  # Here for example, tneve, t1mon and t1yea are disabled.
#  tneve=0
  t5min=300
  t10mi=600
  t1hou=3600
  t1day=86400
  t1wee=604800
#  t1mon=2592000
#  t1yea=31536000

  EXPIRE=$(grep -o '"expire":"[^"]\+"' $TMP-meta | cut -b11-14)
  eval EXPIRES=$(echo \$t$EXPIRE)
  echo $EXPIRES | grep -q . || { rm -rf $TD $TMP*; exit 1; }

  mv $TMP $TD/data
  rm -rf $TMP*
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
