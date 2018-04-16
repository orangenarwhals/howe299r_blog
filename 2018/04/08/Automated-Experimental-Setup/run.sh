#!/bin/bash
APRIL_DIR="/home/nrw/Documents/howe299r/apriltags"
cd $APRIL_DIR
#make clean
make

cd $APRIL_DIR
echo $(pwd)
cd build/bin/
./apriltags_demo
