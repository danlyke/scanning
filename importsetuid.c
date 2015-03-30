#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>

int main(int argc, char *const argv[])
{
    if (setgid( 1003 ))
    {
        perror("setgid failed\n");
        exit(-1);
    }
    if (setuid( 1003 ))
    {
        perror("setuid failed\n");
        exit(-1);
    }
    if (setegid( 1003 ))
    {
        perror("setegid failed\n");
        exit(-1);
    }
    if (seteuid( 1003 ))
    {
        perror("seteuid failed\n");
        exit(-1);
    }


    setenv("HOME", "/home/brscanner", 1);
    chdir("/home/brscanner");
  
    return execv("/home/danlyke/scanning/import.pl", argv);
}
