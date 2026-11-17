-- Log every hit of the ammo instruction (ac_client.exe+C73EF) with its registers: who is firing?
E7LOG = {}
E7N = 0
if not debug_isDebugging() then debugProcess() end
debug_setBreakpoint(0x004C73EF, 1, bptExecute, function()
  E7N = E7N + 1
  local k = string.format("%08X %08X %08X", EDI, EAX, ESI)
  E7LOG[k] = (E7LOG[k] or 0) + 1
  debug_continueFromBreakpoint(co_run)
  return 1
end)
return "watching"
