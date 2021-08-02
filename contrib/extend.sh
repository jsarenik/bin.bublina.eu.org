#!/bin/sh

. ./env
echo Old:
cat env

printf "Enter addition to EXPIRES value (press just ENTER to double it): "
read TTL
test "$TTL" = "" && TTL=$EXPIRES

EXPIRES=$((EXPIRES+TTL))
echo $TTL

{
cat <<EOF
CREATED=$CREATED
EXPIRES=$EXPIRES
EXPIRED=$((CREATED+EXPIRES))
EOF
} | tee env
