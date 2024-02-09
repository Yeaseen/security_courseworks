/* vulnerable2.c */

/* This program has a buffer overflow vulnerability */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int bof(FILE *badfile)
{
	char buffer[24];

	/* The following statement has a buffer overflow problem. */
	fread(buffer, sizeof(char), 60, badfile);

	return 1;
}

int main(int argc, char **argv)
{
	printf("%#x\n",getenv("BINSH"));

	FILE *badfile;
	
	badfile = fopen("./badfile", "r");
	bof(badfile);

	printf("Return Properly\n");

	fclose(badfile);
	return 1;
}
