#! /bin/bash

num=$1
num=${num:=0}
num=${num##0}

nnn=$(printf "%03d" ${num})

[ -f p${nnn}.py ] && exit 2

if [ ${num} -ge 1 -a ${num} -le 999 ]; then

    titre=$(curl -s https://projecteuler.net/problem=${num} | sed -n -e 's?.*<h2>\([^<]*\)</h2>.*?\1?p')

    (echo '"""'
    echo ${titre}
    echo
    echo https://projecteuler.net/problem=${num}
    echo '"""'
    echo ) > p${nnn}.py

    code p${nnn}.py
    # history -s "python3 p${nnn}.py
    echo "Utilisez  python3 p${nnn}.py  pour lancer le programme."
fi
