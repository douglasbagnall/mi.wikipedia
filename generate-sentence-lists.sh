#!/bin/bash

mkdir -p lists
texts="mi-wp-min-500-text-only.txt nga-kōrero-a-reweti-kohere-mā.txt"

for b in '-word-boundaries+-b' '+'; do
    b_switch=${b/*+/}
    b_name=${b/+*/}
    for t in vvv ___ none vv_ _vv; do
        for n in 1 2 5; do
            dest=lists/$b_name-tri-$t-n-$n.txt
            ./find-sentences -n $n -i 20 -b $b_switch -t $t $texts > $dest
        done
    done
done
