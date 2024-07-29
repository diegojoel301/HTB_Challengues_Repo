#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>


void printFile(char *fname)
{
  FILE *file = fopen(fname, "r");
  if(file == NULL)
    error("Failed to open file.");

  int c;
  while((c = fgetc(file)) != EOF)
    printf("%c", (char)c);

  fclose(file);
  exit(0);
}

int main()
{
  printFile("flag.txt");
  return 0;
}
