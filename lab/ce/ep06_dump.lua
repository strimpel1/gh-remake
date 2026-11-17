-- Episode 6: print what ep06_watch.lua logged, and remove its breakpoints.
local s = string.format("player %08X\n", EP06.player or 0)
for _, k in ipairs(EP06.order) do
  local h = EP06.hits[k]
  s = s .. k .. " x" .. h.n .. "\n   " .. h.text .. "\n   " .. h.regs .. "\n"
end
local p = EP06.player
pcall(debug_removeBreakpoint, p + 0x140)
pcall(debug_removeBreakpoint, p + 0xEC)
pcall(debug_removeBreakpoint, p + 0x364)
return s
