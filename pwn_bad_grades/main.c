#include<stdio.h>

int main()
{
  double vector[3];

  double promedio = 0.0;

  for (int i = 0; i < 1; i++)
  {
    scanf("%lf", vector + i);
    promedio += vector[i];  
  }
  printf("%.2f\n", promedio);
}


