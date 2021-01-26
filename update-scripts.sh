#!/bin/sh

wget -O - http://127.0.0.1:8890/index.php \
  | sed \
    -e '1,2d' \
  > gen/index.html

mkdown() {
  a=/$1
  mkdir -p public/${a%/*}
  wget -O public/${a%\?*} http://127.0.0.1:8890/$a
}

catit() {
  cat gen/index.html
}

catit \
  | grep '^\s\+<script' \
  | grep -o 'src="[^"]\+' \
  | cut -b6- \
  | while read a
do mkdown $a; done

catit \
  | grep '^\s\+<link' \
  | grep -o 'href="[^"]\+' \
  | cut -b7- \
  | while read a
do mkdown $a; done
