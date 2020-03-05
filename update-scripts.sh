#!/bin/sh

wget -O - localhost:8890/index.php \
  | grep '^\s\+<script' \
  > gen/scripts.head

grep -o 'src="[^"]\+"' gen/scripts.head \
  | cut -b5- | tr -d '"' \
  | while read a
do
  wget -O public/${a%\?*} http://localhost:8890/$a
done
