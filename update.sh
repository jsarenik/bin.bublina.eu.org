#!/bin/sh

#./genmin.sh
git gc
rsync -av --delete . hd:web/bin/
