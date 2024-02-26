
/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast++ -o harness_fuzzer test_libarchive.c -larchive


/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -i input/ -o findings/ -- ./harness_fuzzer @@
