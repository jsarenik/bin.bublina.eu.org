#!/bin/sh

export PATH=/busybox:$PATH
cd /tmp/bin
for paste in *
do
  test -d $paste/comment || continue
  cd $paste/comment
  for comment in $(ls -rt)
  do
    CREATED=$(stat -c"%Y" $comment)
    TOUCH=$(date -d@$CREATED "+%Y%m%d%H%M.%S")
    ID=$(md5sum $comment | cut -b-16)
    echo ",\"meta\":{\"created\":$CREATED,\"icon\":\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAIAAAC0tAIdAAAABnRSTlMAAAAAAABupgeRAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAQ0lEQVQokWNkgAGHBQkMuMGBhAUMDAxMeFRgAlqqZsQUQvYAxLkUm01+mBxIWIDmBnJcwoJVFJeraBom+IMCDdAy5gEFVRIcKzO8OgAAAABJRU5ErkJggg==\"},\"id\":\"$ID\"" >> $comment
    test "$comment" != "$ID" && mv -v "$comment" "$ID"
    touch -t $TOUCH $ID
  done
  cd /tmp/bin
done
