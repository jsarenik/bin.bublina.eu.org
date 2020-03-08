#!/bin/sh

wget -O gen/index.html http://127.0.0.1:8890/index.php

mkdown() {
  mkdir -p public/${1%/*}
  wget -O public/${1%\?*} http://127.0.0.1:8890/$1
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
