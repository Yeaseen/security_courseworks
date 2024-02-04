# Welcome to Fuzzgoat

This C program has been deliberately backdoored with several memory corruption bugs to test the efficacy of fuzzers and other analysis tools. Each vulnerability is clearly commented in fuzzgoat.c. Under input-files/ are files to trigger each vulnerability.

## Install AFL++

## Building Fuzzgoat

Fuzzgoat builds with make. With afl-gcc in your PATH:

`make`

## Running AFL++ with Source-code instrumentation with afl-gcc

With afl-fuzz in your PATH and a seed file in a directory called in/

`afl-fuzz -i in -o out ./fuzzgoat @@`

or simply:

`make afl`
