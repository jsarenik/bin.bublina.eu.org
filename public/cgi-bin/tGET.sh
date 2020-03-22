echo "Content-Type: text/html; charset=UTF-8"
echo
echo "<!DOCTYPE html>"
test "$HTTP_COOKIE" = "" \
  || eval $(echo "$HTTP_COOKIE" | grep -o '[a-zA-Z]\+=[[:alnum:]]\+')
test -n "$lang" && lang=" lang=\"$lang\""
echo "<html$lang>"
exec cat $HERE/a.html
