#!/bin/bash

mkdir -p notes
text=mi-wp-min-500-text-only.txt

for macrons in macrons+ expanded+-m; do
    m_switch=${macrons/*+/}
    m_name=${macrons/+*/}
    for diphthongs in simple+ diphthong-aware+-d; do
        d_switch=${diphthongs/*+/}
        d_name=${diphthongs/+*/}
        for n in 2 3; do
            fn=notes/$n-gram-$m_name-$d_name.txt
            ./count-ngrams -n $n $m_switch $d_switch $text > $fn
        done
    done
done