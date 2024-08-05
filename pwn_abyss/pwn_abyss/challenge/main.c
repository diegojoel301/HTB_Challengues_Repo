#include<stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>


int main()
{
  int cmd;
  printf("read = %d\n", read(0, &cmd, sizeof(cmd)));
  printf("sizeof = %d\n", sizeof(cmd));
  printf("cmd = %d\n", cmd);

  return 0;
}
