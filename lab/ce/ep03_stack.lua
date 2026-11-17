-- While stopped at a breakpoint: registers and the top of the stack, as text.
local s = string.format("EAX=%08X EBX=%08X ECX=%08X EDX=%08X ESI=%08X EDI=%08X EBP=%08X ESP=%08X EIP=%08X\n", EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP, EIP)
for i = 0, 0x48, 4 do
  local v = readInteger(ESP + i)
  s = s .. string.format("[esp+%02X] %08X = %08X  %s\n", i, ESP + i, v, getNameFromAddress(v) or "")
end
return s
