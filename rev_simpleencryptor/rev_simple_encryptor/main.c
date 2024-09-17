#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef unsigned char byte;  // Define 'byte' como un tipo de dato de un solo byte

int main() {
    FILE *fd = fopen("flag", "rb");
    if (fd == NULL) {
        perror("Error opening file");
        return 1;
    }

    fseek(fd, 0, SEEK_END);
    size_t fd_ptr = ftell(fd);
    fseek(fd, 0, SEEK_SET);  // Rewind to the beginning of the file

    printf("Len: %zu\n", fd_ptr);

    // Size del contenido
    void *ptr = malloc(fd_ptr);
    

    fread(ptr, fd_ptr, 1, fd);
    fclose(fd);

    // Obtener el valor de tiempo actual
    time_t time_val = time(NULL);
    unsigned int u_time = (unsigned int)time_val;

    printf("Time val: %ld\n", (long)time_val);

    srand(u_time);

    byte *data = (byte *)ptr;  // Convierte el puntero a byte

    for (size_t i = 0; i < fd_ptr; i++) {
        int r1 = rand();
        printf("r1 = %d\n", r1);

        data[i] ^= (byte)r1;  // Aplica XOR con el valor aleatorio

        int r2 = rand();
        r2 &= 7;  // Limita r2 a los valores 0-7
        printf("r2 = %d\n", r2);

        // Aplica un desplazamiento circular a la izquierda
        data[i] = (data[i] << r2) | (data[i] >> (8 - r2));
        printf("data[..] = %d\n", data[i]);
    }

    // Aquí puedes guardar el resultado en un archivo o hacer algo con el buffer modificado
    // Por ejemplo, podrías escribir el contenido modificado en un nuevo archivo
    FILE *out_fd = fopen("flag_enc", "wb");
    if (out_fd == NULL) {
        perror("Error opening output file");
        free(ptr);
        return 1;
    }
    
    fwrite(ptr, fd_ptr, 1, out_fd);
    fclose(out_fd);

    free(ptr);
    return 0;
}
