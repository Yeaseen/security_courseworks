#Fuzzing System's libarchive binary shared file in QEMU mode
#for this you need to have clean libarchive installed in a regular path
#in case, you somehow messed up with the system's libarchive

#sudo apt-get install --reinstall libarchive-dev

#Verify that the new version of `libarchive` is correctly installed and recognized
#ldconfig -p | grep libarchive

gcc -o harness_fuzzer test_libarchive.c -larchive
#AFL_INST_LIBS=1 AFL_DEBUG=1 /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -i input/ -o findings/ -- ./harness_fuzzer @@
AFL_INST_LIBS=1 /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -i input/ -o findings/ -- ./harness_fuzzer @@
#AFL_INST_LIBS=1 /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -D -i input/ -o findings/ -- ./harness_fuzzer @@
