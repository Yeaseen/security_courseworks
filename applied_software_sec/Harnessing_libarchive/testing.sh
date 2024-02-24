# Compile a program that uses the libarchive API, linking against the libarchive library
gcc -o test_libarchive test_libarchive.c -larchive

# Run the compiled program, input should be a zip file
./test_libarchive abc.zip

