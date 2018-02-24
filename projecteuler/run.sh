#! /bin/bash

cd build
cmake ..
make
cd -

for i in $(seq -f "%03g" 1 200); do

    if [ -f p${i}.py ]; then
        echo "---------------- problem ${i} (Python) ----------------"
        time -p python3 p${i}.py
    fi

    if [ -f build/p${i} ]; then
        echo "---------------- problem ${i} (C/C++) ----------------"
        time -p build/p${i}
    fi

done