#include<stdio.h>

char buf[0x100] = {0};
FILE *fp;
int main(){

    fp = fopen("flag.txt", "rw");

    gets(buf);

    fclose(fp);
}