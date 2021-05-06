#!/bin/sh

#./genmin.sh
cd gen
./gen.sh
cd ..
git gc
rsync -av --delete . singer:web/bin/
