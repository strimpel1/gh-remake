// scanme.cpp: a tiny console "game" to practise memory scanning on. Yours, offline, nothing to break.
// Game Hacking from Scratch, episode 5.   Build (MSVC):  cl /EHsc scanme.cpp     Run:  scanme.exe
//
//   G  earn gold        the number is on screen: scan for it as an exact value
//   H  take a hit       health is only a bar: scan for it as an unknown value
//   R  rest             health goes back up a little
//   E  use energy       the screen shows 87, but memory holds a float like 87.34
//   Q  quit
//
// "scanme.exe demo" plays a fixed sequence of keys and prints every screen (that is scanme.out.txt).
#include <conio.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <windows.h>

// volatile = always read the value from memory again, so a change made from outside shows up.
struct Player {
    volatile int   gold;      // 4 Bytes
    volatile float health;    // Float, 0 to 100, drawn as a bar with no number
    volatile float energy;    // Float, printed without its fraction
};

struct Hud {
    volatile int shown_gold;  // a display copy: refreshed from player->gold ten times a second
};

static void draw(const Player* p, const Hud* h, bool home) {
    if (home) {
        COORD top = {0, 0};
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), top);
    }
    char bar[21];
    int full = (int)(p->health / 5.0f + 0.5f);
    if (full < 0) full = 0;
    if (full > 20) full = 20;
    for (int i = 0; i < 20; i++) bar[i] = i < full ? '#' : '.';
    bar[20] = 0;
    printf("  SCAN ME            a practice target\n\n");
    printf("  gold     %-10d\n", h->shown_gold);
    printf("  health   [%s]\n", bar);
    printf("  energy   %-10d\n\n", (int)p->energy);
    printf("  G gold   H hit   R rest   E energy   Q quit\n");
}

static bool key(Player* p, int c) {
    switch (c) {
    case 'g': p->gold = p->gold + 7; break;
    case 'h': p->health = p->health - 12.5f; if (p->health < 0) p->health = 0; break;
    case 'r': p->health = p->health + 5.0f; if (p->health > 100) p->health = 100; break;
    case 'e': p->energy = p->energy - 3.3f; if (p->energy < 0) p->energy = 0; break;
    case 'q': return false;
    }
    return true;
}

int main(int argc, char** argv) {
    Player* player = new Player{250, 100.0f, 87.34f};   // on the heap: a new address on every run
    Hud* hud = new Hud{player->gold};

    if (argc > 1 && strcmp(argv[1], "demo") == 0) {
        for (const char* k = " ggher"; *k; k++) {
            key(player, *k);
            hud->shown_gold = player->gold;
            if (*k != ' ') printf("--- key %c\n", *k);
            draw(player, hud, false);
        }
        printf("--- in memory: gold %d, health %.2f, energy %.2f\n", (int)player->gold, (float)player->health, (float)player->energy);
        return 0;
    }

    SetConsoleTitleA("Scan Me");
    system("mode con: cols=54 lines=9");
    for (;;) {
        hud->shown_gold = player->gold;                 // the copy follows the real value, ten times a second
        draw(player, hud, true);
        if (_kbhit() && !key(player, _getch() | 0x20)) break;
        Sleep(100);
    }
    delete hud;
    delete player;
    return 0;
}
