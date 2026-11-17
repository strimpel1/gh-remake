@echo off
rem Builds calls.cpp twice: 64-bit (calls.exe, calls.asm) and 32-bit (calls32.exe, calls32.asm).
setlocal
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /Od /EHsc /FA /Facalls.asm /Fecalls.exe calls.cpp
endlocal
setlocal
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvarsamd64_x86.bat" >nul
cl /nologo /Od /EHsc /FA /Facalls32.asm /Fecalls32.exe /Focalls32.obj calls.cpp
endlocal
