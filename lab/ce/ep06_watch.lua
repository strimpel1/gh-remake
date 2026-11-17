-- Episode 6 (discovery, not on screen): log which instructions ACCESS the magazine, the health and the current-weapon
-- pointer of the local player. Read the result back with ep06_dump.lua. Our own offline AssaultCube only.
EP06 = { hits = {}, order = {} }
local base = getAddress("ac_client.exe")
local player = readInteger(base + 0x17E0A8)
EP06.player = player
local function watch(name, addr, kind)
  debug_setBreakpoint(addr, 4, kind, function()
    local ip = getPreviousOpcode(EIP)
    local key = name .. string.format(" %08X", ip)
    if not EP06.hits[key] then
      EP06.hits[key] = { n = 0, ip = ip, text = disassemble(ip),
        regs = string.format("EAX=%08X EBX=%08X ECX=%08X EDX=%08X ESI=%08X EDI=%08X EBP=%08X", EAX, EBX, ECX, EDX, ESI, EDI, EBP) }
      table.insert(EP06.order, key)
    end
    EP06.hits[key].n = EP06.hits[key].n + 1
    debug_continueFromBreakpoint(co_run)
    return 1
  end)
end
if not debug_isDebugging() then debugProcess() end
local what = EP06_WHAT or "mag"
if what == "mag" then watch("mag", player + 0x140, bptAccess) end
if what == "health" then watch("health", player + 0xEC, bptAccess) end
if what == "weapon" then watch("weapon", player + 0x364, bptAccess) end
return string.format("player %08X watching %s", player, what)
