#!/bin/sh

myget() {
  mkdir -p public/${1%/*}
  wget -c -O public/$1 https://bin.moritz-fromm.de/$1
}

timeout 10 ./run-site.sh 2>&1 | grep -B1 "response:404" | grep url: \
  | cut -d/ -f2- \
  | while read a; do myget $a; done
