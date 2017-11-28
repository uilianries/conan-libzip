#include <stdio.h>
#include <libzip/config.h>

int main(int argc, char *argv[])
{
  /* more exciting tests can be implemented, for now just print the version */
  printf("libzip version %s\n", VERSION);
  return 0;
}

