#!/bin/bash

while :
do
    row=$(( ( RANDOM % 12 ) + 1 + 4 ))
    col=$(( ( RANDOM % 12 ) + 1 + 4 ))
    if [ $(( $row % 2 )) -ne 0 ];
    then
        row=$(( $row + 1 ))
    fi
    if [ $(( $col % 2 )) -ne 0 ];
    then
        col=$(( $col + 1 ))
    fi
    echo $row$'\n'$col$'\n'B$'\n'W$'\n'\>$'\n' | /home/darshan/python3.4.3/bin/python3.4 play_othello.py
    # cat input.txt | /home/darshan/python3.4.3/bin/python3.4 play_othello.py
    echo row: $row col: $col
    sleep 0.5
done
