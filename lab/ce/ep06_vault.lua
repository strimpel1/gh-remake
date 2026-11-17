-- Episode 6 (verification of the practice task, not on screen): attach to vault.exe, log the instruction that writes the coins.
-- EP06V_STEP = 1: set the watch.  2: report the instruction, then who holds the player's address (8 bytes).
if EP06V_STEP == 1 then
  openProcess("vault.exe")
  local base = getAddress("vault.exe")
  local player = readQword(base + 0x23B80)
  EP06V = { player = player, hits = {} }
  debugProcess()
  debug_setBreakpoint(player + 0x14, 4, bptWrite, function()
    local ip = getPreviousOpcode(RIP)
    EP06V.hits[#EP06V.hits + 1] = string.format("%s | RAX=%X RCX=%X RDX=%X", disassemble(ip), RAX, RCX, RDX)
    debug_continueFromBreakpoint(co_run)
    return 1
  end)
  return string.format("player %X coins %d", player, readInteger(player + 0x14))
else
  local s = table.concat(EP06V.hits, "\n") .. "\n"
  pcall(debug_removeBreakpoint, EP06V.player + 0x14)
  local ms = createMemScan()
  ms.firstScan(soExactValue, vtQword, rtRounded, string.format("%d", EP06V.player), "", 0, 0x7fffffffffff, "", fsmNotAligned, "1", false, false, false, false)
  ms.waitTillDone()
  local fl = createFoundList(ms)
  fl.initialize()
  s = s .. fl.Count .. " holders of the player address\n"
  for i = 0, math.min(fl.Count, 20) - 1 do
    local a = tonumber(fl.Address[i], 16)
    s = s .. fl.Address[i] .. "  " .. getNameFromAddress(a) .. (inModule(a) and "  STATIC" or "") .. "\n"
  end
  return s .. "coins now " .. readInteger(EP06V.player + 0x14)
end
