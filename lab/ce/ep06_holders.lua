-- Episode 6 (verification, not on screen): which addresses hold a given 4-byte value (EP06_VALUE)? Lists each one
-- with its module-relative name when it is inside a module. Used to check what the on-screen hex scan will find.
local ms = createMemScan()
ms.firstScan(soExactValue, vtDword, rtRounded, string.format("%d", EP06_VALUE), "", 0, 0x7fffffff, "", fsmNotAligned, "1", false, false, false, false)
ms.waitTillDone()
local fl = createFoundList(ms)
fl.initialize()
local s = string.format("value %08X: %d results\n", EP06_VALUE, fl.Count)
for i = 0, math.min(fl.Count, 60) - 1 do
  local a = tonumber(fl.Address[i], 16)
  s = s .. fl.Address[i] .. "  " .. getNameFromAddress(a) .. (inModule(a) and "  STATIC" or "") .. "\n"
end
fl.destroy()
ms.destroy()
return s
