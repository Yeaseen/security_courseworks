#To compile a libFuzzer-compatible fuzz target to work with AFL++ using the aflpp_driver. 
#This is a common approach when you want to take advantage of AFL++'s features with fuzz targets initially designed for libFuzzer

#You need to have llvm configured afl++

export LLVM_CONFIG=/usr/bin/llvm-config

#Clone AFL++ from github to build from source and go to AFLplusplus/

make all
/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast++ -o fuzz fuzzer_harness.cc /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/libAFLDriver.a -larchive

/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -D -i input -o output_dir -- ./fuzz
