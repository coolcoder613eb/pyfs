#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>

#define fmt "=I"

void get_str(unsigned char *inbytes, int index, char *data) {
    unsigned char byte = inbytes[index];
    int i = 0;
    while (byte != 0) {
        index++;
        data[i++] = (char)byte;
        byte = inbytes[index];
    }
    data[i] = '\0';
}

void writeimg(char *filedir, char *imgfile) {
    char cwd[1024];
    getcwd(cwd, sizeof(cwd));
    chdir(filedir);
    FILE *f;
    unsigned char read[1024];
    unsigned char *files[1024];
    int file_count = 0;
    struct {
        char *filename;
        int length;
        unsigned char *data;
    } binfiles[1024];

    DIR *dir = opendir(".");
    struct dirent *ent;
    if (dir != NULL) {
        while ((ent = readdir(dir)) != NULL) {
            if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0) {
                continue;
            }

            char filepath[1024];
            snprintf(filepath, sizeof(filepath), "%s/%s", filedir, ent->d_name);
            f = fopen(ent->d_name, "rb");
            if (f != NULL) {
                size_t read_size = fread(read, sizeof(unsigned char), sizeof(read), f);
                fclose(f);
                unsigned char *file = malloc(strlen(ent->d_name) + 1 + 4 + read_size);
                strcpy(file, ent->d_name);
                strcat(file, "\0");
                memcpy(file + strlen(ent->d_name) + 1, &read_size, 4);
                memcpy(file + strlen(ent->d_name) + 1 + 4, read, read_size);
                files[file_count++] = file;
            }
        }
        closedir(dir);
    }

    unsigned char *data = malloc(file_count * sizeof(unsigned char *));
    memcpy(data, files, file_count * sizeof(unsigned char *));
    chdir(cwd);

    f = fopen(imgfile, "wb");
    if (f != NULL) {
        fwrite(data, sizeof(unsigned char), file_count * sizeof(unsigned char *), f);
        fclose(f);
    }

    for (int i = 0; i < file_count; i++) {
        free(files[i]);
    }
    free(data);
}

void readimg(char *filedir, char *imgfile) {
    char cwd[1024];
    getcwd(cwd, sizeof(cwd));
    FILE *f = fopen(imgfile, "rb");
    if (f != NULL) {
        fseek(f, 0, SEEK_END);
        long img_size = ftell(f);
        rewind(f);
        unsigned char *read = malloc(img_size);
        size_t read_size = fread(read, sizeof(unsigned char), img_size, f);
        fclose(f);

        int index = 0;
        struct {
            char filename[1024];
            int length;
            unsigned char *data;
        } files[1024];
        int file_count = 0;

        while (index < read_size) {
            get_str(read, index, files[file_count].filename);
            index += strlen(files[file_count].filename) + 1;
            memcpy(&files[file_count].length, read + index, 4);
            index += 4;
            files[file_count].data = malloc(files[file_count].length);
            memcpy(files[file_count].data, read + index, files[file_count].length);
index += files[file_count].length;
file_count++;
}

    chdir(filedir);
    for (int i = 0; i < file_count; i++) {
        FILE *outfile = fopen(files[i].filename, "wb");
        if (outfile != NULL) {
            fwrite(files[i].data, sizeof(unsigned char), files[i].length, outfile);
            fclose(outfile);
        }
        free(files[i].data);
    }
    chdir(cwd);

    free(read);
}

}

int main() {
char filedir[] = "files";
char imgfile[] = "image.img";
writeimg(filedir, imgfile);
printf("Image file created!\n");


char outdir[] = "output";
readimg(outdir, imgfile);
printf("Image file read and files extracted!\n");

return 0;

}
