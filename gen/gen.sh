#!/bin/sh

for i in a b notdeleted
do
  cat \
    begin.html \
    status-${i}.html \
    rest.html \
    end.html \
    > ../public/cgi-bin/${i}.html
done
