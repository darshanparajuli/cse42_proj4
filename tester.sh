#!/bin/bash

for i in `seq 1 100`;
do
    cat input.txt | /home/darshan/python3.4.3/bin/python3.4 play_othello.py
    sleep 0.5
done