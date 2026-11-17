-- Print the log of ep07_log.lua: EDI (owner), EAX (address written), ESI (weapon), hits; then every player's magazine.
local s = string.format("local player %08X\n", readInteger(0x0057E0A8))
for k, v in pairs(E7LOG or {}) do
  local edi, eax = tonumber(k:sub(1, 8), 16), tonumber(k:sub(10, 17), 16)
  s = s .. k .. " hits " .. v .. string.format("  eax-edi=%X  value now %d  name %s\n", eax - edi, readInteger(eax), readString(edi + 0x205, 16) or "?")
end
return s .. "total " .. tostring(E7N)
