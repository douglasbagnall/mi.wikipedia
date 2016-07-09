#!/bin/bash

mkdir -p notes
texts="mi-wp-min-500-text-only.txt nga-kōrero-a-reweti-kohere-mā.txt"

for macrons in macrons+ expanded+-m; do
    m_switch=${macrons/*+/}
    m_name=${macrons/+*/}
    for diphthongs in simple+ diphthong-aware+-d; do
        d_switch=${diphthongs/*+/}
        d_name=${diphthongs/+*/}
        for n in 2 3; do
            for b in '-word-boundaries+-b' '+'; do
                b_switch=${b/*+/}
                b_name=${b/+*/}
                fn=notes/$n-gram-$m_name-$d_name$b_name.txt
                ./count-ngrams -n $n $m_switch $d_switch $b_switch $texts > $fn
            done
        done
    done
done
