// Episode 3 practice program: a few lines of C++ to read back as assembly.
//
//   cl /Od /FA calls.cpp      builds calls.exe and writes the listing calls.asm
// (Which prompt to run it in, and a note on the practice task: at the end of this file.)
// Open calls.asm next to this file and find each line of C++ in it.
#include <cstddef>
#include <cstdio>

struct Player {
    int id;
    int health;
    int ammo;
    void hit(int damage);
};

int add3(int a, int b, int c) {
    int sum = a + b + c;
    return sum;
}

void Player::hit(int damage) {
    health = health - damage;
    if (health <= 0)
        std::puts("dead");
}

int main() {
    Player p = {7, 100, 20};
    int s = add3(1, 2, 3);
    p.hit(30);
    std::printf("sum %d  health %d\n", s, p.health);
    std::printf("offset of health: %X   offset of ammo: %X\n",
                (unsigned)offsetof(Player, health), (unsigned)offsetof(Player, ammo));
}

// Notes (kept down here so the line numbers in the listing stay the same as in the video).
//
// Which prompt: the video reads the 32-bit listing. Run cl in the "x86 Native Tools Command Prompt
// for VS" to get it. In the 64-bit (x64) prompt the same command writes a listing like the 64-bit
// part of the video: arguments in rcx, rdx and r8 instead of pushes.
//
// Practice (add an int field above health): the three numbers in  Player p = {7, 100, 20};  then
// land one field earlier: the new field gets 100, health gets 20 and ammo gets 0. So the program
// prints "dead" and "sum 6  health -10" before the offsets. That is correct, not a bug. Add a
// fourth number, for example {7, 0, 100, 20}, if you want health to be 100 again. Either way the
// last line, "offset of health: ...", is your answer key.
