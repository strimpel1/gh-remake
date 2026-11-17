// Episode 4: the same EXE, once as a file on disk and once as a running process.
// Prints where this program was loaded, the first bytes found there, and every module in the process.
#include <cstdio>
#include <windows.h>
#include <psapi.h>

int main() {
    auto base = (unsigned char*)GetModuleHandle(nullptr);

    std::printf("process id        %lu\n", GetCurrentProcessId());
    std::printf("thread id         %lu\n", GetCurrentThreadId());
    std::printf("loaded at         %012llX\n", (unsigned long long)base);
    std::printf("first bytes there %02X %02X  \"%c%c\"\n", base[0], base[1], base[0], base[1]);

    HMODULE mods[256];
    DWORD bytes = 0;
    K32EnumProcessModules(GetCurrentProcess(), mods, sizeof mods, &bytes);
    std::printf("modules in this process:\n");
    for (unsigned i = 0; i < bytes / sizeof(HMODULE); i++) {
        char name[MAX_PATH];
        GetModuleBaseNameA(GetCurrentProcess(), mods[i], name, sizeof name);
        std::printf("  %012llX  %s\n", (unsigned long long)mods[i], name);
    }
}
