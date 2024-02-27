
#First run `build_libarchive_cmake`
#Now look for libarchive.so file
find /mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive -name libarchive.so

#Makw sure that you exported the shared library path to the LD_LIBRARY_PATH environment variable before running harness_fuzzer2. This tells the runtime linker to look in the additional directory for shared libraries.
export LD_LIBRARY_PATH=/mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive/libarchive_install/lib/:$LD_LIBRARY_PATH


#pass the location of libarchive.so here
/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast -o harness_fuzzer2 test_libarchive.c -L libarchive/libarchive_install/lib/ -l archive -I libarchive/libarchive_install/lib/ -fsanitize=address 

#the following command is for checking which dll the binary is using
ldd harness_fuzzer2
#the following command is for checking whether the library file actually instrumented by afl
objdump -D /mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive/libarchive_install/lib/libarchive.so | grep afl

#Now start fuzzing and have fun
/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -i input/ -o findings/ -- ./harness_fuzzer2 @@

