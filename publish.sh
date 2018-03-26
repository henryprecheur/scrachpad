#!/bin/sh

cd /var/www/henry.precheur.org/scratchpad/

readonly dir=.log
test -d $dir || mkdir $dir

{
    cat; echo 
} | tee -a log $dir/$(date +%s)

readonly python=.env/bin/python

$python html.py < log
$python atom.py < log > feed.atom
