#!/bin/sh

readonly url='https://github.com/pypa/virtualenv/archive/1.10.1.tar.gz'

readonly tmp=$(mktemp -d)
trap "rm -rf $tmp" ERR

cd $tmp
curl -s --location $url | tar zxf -
cd *
readonly python=${PYTHON:=python}
$python virtualenv.py $@
