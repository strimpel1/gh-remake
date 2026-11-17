// Episode 3 practice program: a few lines of C++ to read back as assembly.
//
//   cl /Od /FA calls.cpp      builds calls.exe and writes the listing calls.asm
//
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
