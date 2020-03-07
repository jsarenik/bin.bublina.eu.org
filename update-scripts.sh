#!/bin/sh

wget -O - http://127.0.0.1:8890/index.php \
  | grep '^\s\+<script' \
  | grep -o 'src="[^"]\+"' \
  | cut -b5- | tr -d '"' \
  | while read a
do
  wget -O public/${a%\?*} http://127.0.0.1:8890/$a
done

wget -O gen/index.html http://127.0.0.1:8890/index.php
