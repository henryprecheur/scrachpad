#!/bin/sh

cd /var/www/henry.precheur.org/scratchpad/

readonly dir=.log
test -d $dir || mkdir $dir

tmp=$(date +%FT%T%z | sed 's/\([+-][01][0-9]\)\([0-9][0-9]\)$/\1:\2/')
{ cat; echo  } | tee -a log $dir/$tmp

if test -x ./python
then
    python=./python
else
    python=python
fi
python=.env/bin/python

$python html.py < log > index.html
$python atom.py < log > feed.atom
