#!/bin/bash
function levenshtein {
    if (( $# != 2 )); then
        echo "Usage: $0 word1 word2" >&2
    elif (( ${#1} < ${#2} )); then
        levenshtein "$2" "$1"
    else
        local str1len=${#1}
        local str2len=${#2}
        local d

        for i in $( seq 0 $(( (str1len+1)*(str2len+1) )) ); do
            d[i]=0
        done

        for i in $( seq 0 $str1len );	do
            d[i+0*str1len]=$i
        done

        for j in $( seq 0 $str2len );	do
            d[0+j*(str1len+1)]=$j
        done

        for j in $( seq 1 $str2len ); do
            for i in $( seq 1 $str1len ); do
                [ "${1:i-1:1}" = "${2:j-1:1}" ] && local cost=0 || local cost=1
                del=$(( d[(i-1)+str1len*j]+1 ))
                ins=$(( d[i+str1len*(j-1)]+1 ))
                alt=$(( d[(i-1)+str1len*(j-1)]+cost ))
                d[i+str1len*j]=$( echo -e "$del\n$ins\n$alt" | sort -n | head -1 )
            done
        done
        echo "${d[str1len+str1len*(str2len)]} $1 $2"
    fi
}

levenshtein $1 $2
