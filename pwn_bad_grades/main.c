#include <stdio.h>
#include <string.h>

int main() {
    // Valor hexadecimal para 1.0 en double: 0x3ff0000000000000
    unsigned char hex_bytes[] = {0x63, 0x12, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00}; // Little-endian order
    double x;

    memcpy(&x, hex_bytes, sizeof(double));

    printf("El valor de x en decimal es: %f\n", x);

    return 0;
}

