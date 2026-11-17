-- Episode 3 check: when the magazine is decremented (ac_client.exe+C73EF), is ESI the player's current weapon, [player+364]?
EP03V = { n = 0 }
local base = getAddress("ac_client.exe")
local player = readInteger(base + 0x17E0A8)
if not debug_isDebugging() then debugProcess() end
debug_setBreakpoint(player + 0x140, 4, bptWrite, function()
  EP03V.n = EP03V.n + 1
  EP03V.s = string.format("ip %08X  ESI %08X  [player+364] %08X  [esi+14] %08X  player+140 %08X  EDI %08X player %08X",
    getPreviousOpcode(EIP), ESI, readInteger(player + 0x364), readInteger(ESI + 0x14), player + 0x140, EDI, player)
  debug_continueFromBreakpoint(co_run)
  return 1
end)
return string.format("watching %08X", player + 0x140)
