#Fuzzing System's libarchive binary shared file in QEMU mode
#for this you need to have clean libarchive installed in a regular path
#in case, you somehow messed up with the system's libarchive
sudo apt-get install --reinstall libarchive-dev

gcc -o harness_fuzzer test_libarchive.c -larchive
AFL_INST_LIBS=1 /mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -i input/ -o findings/ -- ./harness_fuzzer @@
