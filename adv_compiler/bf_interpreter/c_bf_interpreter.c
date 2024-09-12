#include <stdio.h>
#include <stdlib.h>

#define TAPE_SIZE 30000

int main() {
    unsigned char tape[TAPE_SIZE] = {0};
    unsigned char* ptr = tape;
    char* buffer = NULL;
    size_t bufsize = 0;
    size_t input_length = getdelim(&buffer, &bufsize, EOF, stdin);
    if (input_length == -1) return 1;

    for (int i = 0, loop = 0; i < input_length; i++) {
        switch (buffer[i]) {
            case '>': if (ptr < tape + TAPE_SIZE - 1) ++ptr; break;
            case '<': if (ptr > tape) --ptr; break;
            case '+': ++*ptr; break;
            case '-': --*ptr; break;
            case '.': putchar(*ptr); break;
            case ',': *ptr = getchar(); break;
            case '[':
                if (!*ptr) {
                    loop = 1;
                    while (loop > 0) {
                        ++i;
                        if (buffer[i] == '[') ++loop;
                        if (buffer[i] == ']') --loop;
                    }
                }
                break;
            case ']':
                if (*ptr) {
                    loop = 1;
                    while (loop > 0) {
                        --i;
                        if (buffer[i] == '[') --loop;
                        if (buffer[i] == ']') ++loop;
                    }
                }
                break;
        }
    }

    free(buffer);
    return 0;
}
