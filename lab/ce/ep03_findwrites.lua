-- Add a plain record for the magazine address of this run and open "Find out what writes to this address" on it.
local base = getAddress("ac_client.exe")
local player = readInteger(base + 0x17E0A8)
local al = getAddressList()
local mr = EP03_MR
if not mr then
  mr = al.createMemoryRecord()
  mr.Description = "magazine (this run's address)"
  mr.Address = string.format("%08X", player + 0x140)
  mr.Type = vtDword
  EP03_MR = mr
end
al.SelectedRecord = mr
if not debug_isDebugging() then debugProcess() end
createTimer(300, function() getMainForm().Setbreakpoint1.doClick() end)
return mr.Address
