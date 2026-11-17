// Episode 4 practice program: a tiny "game" that keeps its state in a save file.
//
//   savegame new     write a fresh save.dat (health 100, gold 1000, name Hero) and print it
//   savegame         load save.dat and print what is in it
//
// Open save.dat in a hex editor between the two runs, change some bytes, and load it again.
#include <cstdio>
#include <cstring>

struct Save {
    char magic[4];    // offset 00: the letters S A V E, so we can recognise our own file
    int  health;      // offset 04: 4 bytes, little endian
    int  gold;        // offset 08: 4 bytes, little endian
    char name[16];    // offset 0C: text, padded with zero bytes
};                    // 28 bytes in total

void show(const Save& s) {
    std::printf("health  %d\n", s.health);
    std::printf("gold    %d\n", s.gold);
    std::printf("name    %.16s\n", s.name);
}

int main(int argc, char** argv) {
    const char* path = "save.dat";
    Save s = {};

    if (argc > 1 && std::strcmp(argv[1], "new") == 0) {
        std::memcpy(s.magic, "SAVE", 4);
        s.health = 100;
        s.gold = 1000;
        std::strcpy(s.name, "Hero");
        FILE* f = std::fopen(path, "wb");
        if (!f) { std::printf("cannot create %s\n", path); return 1; }
        std::fwrite(&s, sizeof s, 1, f);
        std::fclose(f);
        std::printf("wrote %s (%d bytes)\n", path, (int)sizeof s);
        show(s);
        return 0;
    }

    FILE* f = std::fopen(path, "rb");
    if (!f) { std::printf("no %s yet: run \"savegame new\" first\n", path); return 1; }
    size_t got = std::fread(&s, 1, sizeof s, f);
    std::fclose(f);
    if (got != sizeof s || std::memcmp(s.magic, "SAVE", 4) != 0) {
        std::printf("%s is not a save file of this game\n", path);
        return 1;
    }
    std::printf("loaded %s (%d bytes)\n", path, (int)got);
    show(s);
}
