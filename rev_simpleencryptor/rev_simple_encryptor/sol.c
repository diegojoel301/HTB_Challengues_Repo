#include<stdlib.h>
#include<stdio.h>
#include <time.h>

typedef unsigned char byte; 

int gray2binary(int x, int s)
{
    int shiftamount = s;
    while(x >> shiftamount)
    {
        x ^= x >> shiftamount;
        shiftamount <<= s;
    }
    return x;
}

int main()
{    

    /*
    def unsigned_char(value):
    # Garantiza que el valor esté entre 0 y 255
    return value & 0xFF
    
r1 = 2312312
r2 = 4

val = 67

x = (val ^ r1) << r2 | (val ^ r1) >> (8 - r2)

x = unsigned_char(x)

print(x)
res = x >> r2 | x << (8 - r2)
res ^= r1
print(unsigned_char(res))
*/
    /*
    Modify: 2022-07-19 07:14:48.000000000 -0400
    1657782888
    */
    /*
    En realidad luego de otro analisis lo saque de aqui xd:
    ❯ xxd flag_true.enc
        00000000: 5a35 b162....
        >>> 0x62b1355a
        1655780698
    */
    uint u_time = 1655780698;
    //uint u_time = 1726587270;

    // El sed ya lo tienes en la fecha de creacion del fichero flag.enc xD

    srand(u_time);

    //FILE *fd = fopen("flag_enc", "rb");
    FILE *fd = fopen("flag_true.enc", "rb");

    fseek(fd, 0, SEEK_END);
    size_t size_ptr = ftell(fd);
    fseek(fd, 0, SEEK_SET);  // Rewind to the beginning of the file

    void *ptr = malloc(size_ptr);

    fread(ptr, size_ptr, 1, fd);
    fclose(fd);

    byte *data = (byte *)ptr;

    // Empiezas en 4 debido a que los primeros 4 bytes son del date en timestamp

    for(int i = 4; i < size_ptr; i++)
    {
        int r1 = rand();
        int r2 = rand();
        r2 = r2 & 7;
 
        //printf("r1 = %d\n", r1);
        //printf("r2 = %d\n", r2);

        data[i] = (data[i] >> r2) | (data[i] << (8 - r2));
        data[i] ^= r1;

        printf("%c", data[i]);   
    }

    

    return 0;
}