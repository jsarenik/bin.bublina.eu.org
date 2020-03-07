#!/bin/sh

for i in a b notdeleted
do
  REPL=$(cat status-$i.html)
  sed "/^\s\+<div id=\"status\"/,/^\s\+<\/div>/c$REPL" index.html \
    > ../public/cgi-bin/${i}.html
done
