#!/bin/sh

for i in js/privatebin.js
do
  MD5=$(md5sum public/$i | cut -b-32)
  EXT=${i##*.}
  N=${i%%.$EXT}
  rm -v public/$N-*
  NN="${N}-${MD5}.$EXT"
  cp public/$i public/$NN
  sed -i "s|$N[^\"]\+|$NN|" gen/index.html
done
