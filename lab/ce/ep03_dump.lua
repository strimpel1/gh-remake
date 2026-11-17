local s = string.format("player %08X\n", EP03.player or 0)
for _, k in ipairs(EP03.order) do
  local h = EP03.hits[k]
  s = s .. k .. " x" .. h.n .. "\n   " .. h.text .. "\n   " .. h.regs .. "\n"
end
return s
