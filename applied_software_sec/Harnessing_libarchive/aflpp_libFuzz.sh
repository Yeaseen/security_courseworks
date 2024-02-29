#To compile a libFuzzer-compatible fuzz target to work with AFL++ using the aflpp_driver. 
#This is a common approach when you want to take advantage of AFL++'s features with fuzz targets initially designed for libFuzzer

#You need to have llvm configured afl++

#export LLVM_CONFIG=/usr/bin/llvm-config

#Clone AFL++ from github to build from source and go to AFLplusplus/

#make all

export LD_LIBRARY_PATH=/mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive/libarchive_install/lib/:$LD_LIBRARY_PATH

/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast++ -o fuzzer_harness fuzzer_harness.cc /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/libAFLDriver.a -L libarchive/libarchive_install/lib/ -l archive -I libarchive/libarchive_install/lib/ -fsanitize=address

#the following command is for checking which dll the binary is using
#ldd fuzzer_harness
#the following command is for checking whether the library file actually instrumented by afl
#objdump -D /mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive/libarchive_install/lib/libarchive.so | grep afl


/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -i input -o output_dir -- ./fuzzer_harness @@
