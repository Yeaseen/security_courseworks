#Fuzzing System's libarchive binary shared file in QEMU mode
#for this you need to have clean libarchive installed in a regular path
#in case, you somehow messed up with the system's libarchive
sudo apt-get install --reinstall libarchive-dev

gcc -o harness_fuzzer test_libarchive.c -larchive
AFL_INST_LIBS=1 /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -i input/ -o findings/ -- ./harness_fuzzer @@


#If you instrumented the system's libarchive shared library (*.so file) in QEMU mode 
#using AFL (American Fuzzy Lop) yesterday, then the libarchive on your system is currently 
#AFL-instrumented. This means that the library has been modified to include AFL's instrumentation 
#code, which is used for fuzz testing by monitoring the code paths that are executed during 
#runtime. The AFL instrumentation is designed to help identify inputs that can trigger bugs 
#or unexpected behavior in the program being fuzzed.

#However, this instrumentation can lead to compatibility issues with applications or 
#build processes that are not part of the fuzz testing setup, as you've experienced. 
#The instrumented library expects certain AFL-specific symbols and runtime support, 
#which are not present when running applications normally or using build tools like CMake 
#in a standard environment.

#so reinstall the system's shared library file of libarchive for further use of make or something