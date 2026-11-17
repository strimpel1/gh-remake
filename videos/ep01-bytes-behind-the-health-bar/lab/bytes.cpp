// Episode 1 practice program: print the bytes a value really occupies in memory.
#include <cstdio>
#include <cstring>

template <class T>
void dump(const char* label, T value) {
    unsigned char bytes[sizeof(T)];
    std::memcpy(bytes, &value, sizeof(T));
    std::printf("%-16s", label);
    for (unsigned char b : bytes) std::printf("%02X ", b);
    std::printf("\n");
}

int main() {
    dump("char 100", (char)100);
    dump("short 100", (short)100);
    dump("int 100", 100);
    dump("int 1000", 1000);
    dump("int 300", 300);        // the practice question: predict this line first
    dump("int -1", -1);
    dump("float 100.0", 100.0f);
    dump("float 43.0", 43.0f);
    dump("double 43.0", 43.0);

    int health = 100;
    float as_float;
    std::memcpy(&as_float, &health, 4);          // same four bytes, read as a float
    std::printf("int 100 read as a float: %g\n", as_float);

    float x = 43.0f;
    int as_int;
    std::memcpy(&as_int, &x, 4);                 // same four bytes, read as an integer
    std::printf("float 43.0 read as an int: %d\n", as_int);
}
