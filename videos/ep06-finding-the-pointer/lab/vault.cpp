// vault.cpp - practice target for "Game Hacking from Scratch" episode 6: Finding the Pointer.
//
// The coins live in a Player object on the heap, so their address is different on every run.
// The program reaches them through one global pointer, g_player, which sits at a fixed offset
// inside vault.exe. Your job, with Cheat Engine:
//   1. find the coins with a normal scan (4 Bytes; press s to spend, Next Scan)
//   2. "Find out what writes to this address", spend once, read the offset and the register
//   3. scan for the register's value (Hex ticked, 8 Bytes: this is a 64-bit program)
//      and pick the green result, vault.exe+something
//   4. Add Address Manually, Pointer: that green address, plus the offset
//   5. save the table, close vault.exe, start it again, load the table: still the coins?
// Press t at any time and the program tells you the truth, so you can check every step.
//
// Build (MSVC):  cl /EHsc vault.cpp        Run: vault.exe
#include <windows.h>
#include <cstdio>
#include <cstdlib>
#include <ctime>

struct Player {
    char name[16];   // +0x00
    int  health;     // +0x10
    int  coins;      // +0x14
    int  keys;       // +0x18
};

Player* g_player = nullptr;      // the static pointer: lives inside vault.exe

__declspec(noinline) void spend(Player* p, int price) {
    p->coins -= price;           // the instruction "Find out what writes" will show you
}

void truth() {
    unsigned long long base = (unsigned long long)GetModuleHandleA(nullptr);
    unsigned long long gp = (unsigned long long)&g_player;
    unsigned long long pl = (unsigned long long)g_player;
    printf("  module base     %012llX\n", base);
    printf("  &g_player       %012llX  = vault.exe+%llX\n", gp, gp - base);
    printf("  player (heap)   %012llX\n", pl);
    printf("  &player->coins  %012llX  = player+%llX\n", (unsigned long long)&g_player->coins,
           (unsigned long long)&g_player->coins - pl);
    printf("  pointer to save: [vault.exe+%llX]+%llX\n", gp - base, (unsigned long long)&g_player->coins - pl);
}

int main() {
    SetConsoleTitleA("Vault");
    // a few allocations of a size that depends on the clock, so the heap layout differs between runs
    srand((unsigned)time(nullptr) ^ GetCurrentProcessId());
    for (int i = 0; i < 8; ++i) (void)malloc(64 + rand() % 4096);
    g_player = new Player{"hero", 100, 500, 3};

    printf("=== Vault: practice target for episode 6 ===\n");
    printf("[s] spend 7 coins   [t] tell the truth   [q] quit\n\n");
    for (;;) {
        printf("coins: %d\n> ", g_player->coins);
        fflush(stdout);
        int c = getchar();
        while (c == '\n' || c == '\r' || c == ' ') c = getchar();
        if (c == EOF || c == 'q') break;
        if (c == 's') spend(g_player, 7);
        if (c == 't') truth();
    }
    return 0;
}
