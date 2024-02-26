#include <archive.h>
#include <archive_entry.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    struct archive *a;
    struct archive_entry *entry;
    int r;

    if(argc != 2) {
        fprintf(stderr, "Usage: %s <archive_file>\n", argv[0]);
        return 1;
    }

    a = archive_read_new();
    archive_read_support_format_all(a);
    r = archive_read_open_filename(a, argv[1], 10240); // Note: 10240 is the size of the buffer
    if (r != ARCHIVE_OK) {
        return 1;
    }
    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        printf("%s\n", archive_entry_pathname(entry));
        archive_read_data_skip(a);  // We're not extracting files here
    }
    archive_read_free(a);
    return 0;
}

