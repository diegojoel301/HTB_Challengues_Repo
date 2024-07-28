#include <stdio.h>
#include <stdlib.h>

void f(int target_value)
{
    unsigned int seed;
    int found = 0;

    for (seed = 0; seed <= 0xFFFFFFFF; seed++) {
        srand(seed);
        if (rand() == target_value) {
             printf("%c%c%c%c", (seed >> 24) & 0xFF, (seed >> 16) & 0xFF, (seed >> 8) & 0xFF, seed & 0xFF);
            found = 1;
            break;
        }
    }
}


int main()
{

    int v[] = {0x244b28be, 0x0af77805, 0x110dfc17, 0x07afc3a1, 0x6afec533, 0x4ed659a2, 0x33c5d4b0, 
               0x286582b8, 0x43383720, 0x055a14fc, 0x19195f9f, 0x43383720, 0x19195f9f, 0x747c9c5e,
               0x0f3da237, 0x615ab299, 0x6afec533, 0x43383720, 0x0f3da237, 0x6afec533, 0x615ab299,
               0x286582b8, 0x055a14fc, 0x3ae44994, 0x06d7dfe9, 0x4ed659a2, 0x0ccd4acd, 0x57d8ed64,
               0x615ab299, 0x22e9bc2a};
    int length = sizeof(v) / sizeof(v[0]);

    for(int i = 0; i < length; i++)
    {
        f(v[i]);
    }


    return 0;
}

