#!/bin/sh

cd /var/www/henry.precheur.org/scratchpad/

readonly dir=.log
test -d $dir || mkdir $dir

{
    cat; echo 
} | tee -a log $dir/$(date +%s)

./scratchpad < log
