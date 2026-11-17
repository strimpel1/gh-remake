-- Episode 3: log which instructions write to the magazine and to the health of the local player.
-- Results go to the global table EP03 (read it back with ep03_dump.lua). Our own offline AssaultCube only.
if not EP03 then EP03 = { hits = {}, order = {} } end
local base = getAddress("ac_client.exe")
local player = readInteger(base + 0x17E0A8)
EP03.player = player
local function watch(name, addr, kind)
  debug_setBreakpoint(addr, 4, kind, function()
    local ip = getPreviousOpcode(EIP)
    local key = name .. string.format(" %08X", ip)
    if not EP03.hits[key] then
      EP03.hits[key] = { n = 0, ip = ip, text = disassemble(ip),
        regs = string.format("EAX=%08X EBX=%08X ECX=%08X EDX=%08X ESI=%08X EDI=%08X EBP=%08X ESP=%08X EIP=%08X", EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP, EIP) }
      table.insert(EP03.order, key)
    end
    EP03.hits[key].n = EP03.hits[key].n + 1
    debug_continueFromBreakpoint(co_run)
    return 1
  end)
end
if not debug_isDebugging() then debugProcess() end
watch("mag", player + 0x140, bptWrite)
watch("health", player + 0xEC, bptWrite)
return string.format("player %08X watching", player)
