-- Add a plain record for the health address of this run and open "Find out what accesses this address" on it.
local base = getAddress("ac_client.exe")
local player = readInteger(base + 0x17E0A8)
pcall(debug_removeBreakpoint, player + 0xEC)
local al = getAddressList()
local mr = EP03_MRH
if not mr then
  mr = al.createMemoryRecord()
  mr.Description = "health (this run's address)"
  mr.Address = string.format("%08X", player + 0xEC)
  mr.Type = vtDword
  EP03_MRH = mr
end
al.SelectedRecord = mr
createTimer(300, function() getMainForm().Findoutwhataccessesthisaddress1.doClick() end)
return mr.Address
