#!/bin/sh

for i in a b notdeleted
do
  cat ${i}.html end.html > ../public/cgi-bin/${i}.html
done
