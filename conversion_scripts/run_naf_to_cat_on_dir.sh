#!/bin/bash

for f in $1*
do
bn=$(basename $f)
cat $f | python naf_to_cat_factuality.py > $2/$bn.xml
done
