CC=/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-gcc
DEPS=main.c fuzzgoat.c
ASAN=-fsanitize=address
CFLAGS=-I.
LIBS=-lm

all: $(DEPS)
	$(CC) -o fuzzgoat $(CFLAGS) $^ $(LIBS)
	gcc -o fuzzgoatQ $(CFLAGS) $^ $(LIBS)
	$(CC) $(ASAN) -o fuzzgoat_ASAN $(CFLAGS) $^ $(LIBS)
	

afl: fuzzgoat
	/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -i in -o out ./fuzzgoat @@

aflASN: fuzzgoatASAN
	/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -i in -o outASAN ./fuzzgoat_ASAN @@

aflQ: fuzzgoatQ
	/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-fuzz -Q -i in -o outQ ./fuzzgoatQ @@

aflMap: fuzzgoat
	/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-showmap -o output.map -m none -- ./fuzzgoat < in/seed

.PHONY: clean

clean:
	rm ./fuzzgoat ./fuzzgoat_ASAN
