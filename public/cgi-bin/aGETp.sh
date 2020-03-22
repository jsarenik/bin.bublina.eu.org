echo "Content-Type: application/json; charset=UTF-8"
echo
NOW=$(date +%s)
TD=$WHERE/$pasteid
. $TD/env
TTL=$((CREATED+EXPIRES-NOW))
# Following line is not needed because TTL will be negative
# when EXPIRES is 0
#test $EXPIRES -eq 0 && TTL=0
echo "{\"status\":0,\"id\":\"$pasteid\",\"url\":\"/?$pasteid\",\
$(cat $TD/data),\"meta\":{\"created\":$CREATED,\"time_to_live\":$TTL},"

if
  ! test -d $TD/comment
then
  echo "\"comments\":[],\"comment_count\":0,\"comment_offset\":0,\
\"@context\":\"?jsonld=paste\"\
}"
else
COMMENTS=$(ls -rt $TD/comment)
NUM=$(echo $COMMENTS | wc -w)
echo "\"comment_count\":$NUM,\"comment_offset\":0,\
\"@context\":\"?jsonld=paste\",\"comments\":["
for i in $COMMENTS
do test "$A" = "" && { echo "{"; A=1; } || echo ",{"
  cat $TD/comment/$i; echo "}"
done
echo "]}"
fi

grep -oqF '0,1]' $TD/data && rm -rf $TD
