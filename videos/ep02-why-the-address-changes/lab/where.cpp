// Episode 2 practice program: where do things live, and does it change between runs?
#include <cstdio>
#include <windows.h>

struct Player {
    int health = 100;
    int ammo = 20;
};

Player* g_player = nullptr;   // a global pointer: it lives inside the module

int main() {
    g_player = new Player;    // the player itself lives on the heap
    int local = 7;            // a local variable lives on the stack

    auto base = (unsigned long long)GetModuleHandle(nullptr);
    auto global = (unsigned long long)&g_player;

    std::printf("module base       %012llX\n", base);
    std::printf("&g_player         %012llX   = base + %llX\n", global, global - base);
    std::printf("player (heap)     %012llX\n", (unsigned long long)g_player);
    std::printf("local (stack)     %012llX\n", (unsigned long long)&local);
    std::printf("health through the pointer: %d\n", g_player->health);
}
