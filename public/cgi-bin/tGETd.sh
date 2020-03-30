echo "Content-Type: text/html; charset=UTF-8"
echo
echo "<!DOCTYPE html>"
echo "<html>"
TD=$WHERE/$pasteid
. $TD/env
. $TD/dt
test "$deletetoken" = "$DT" \
  && { rm -rf $TD; exec cat $HERE/b.html; } \
  || exec cat $HERE/notdeleted.html
