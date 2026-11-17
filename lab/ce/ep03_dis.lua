-- Disassemble a range to lab/ce/dis.txt. Set EP03_FROM / EP03_TO first (globals), or the defaults are used.
local a, b = EP03_FROM or 0x004C7300, EP03_TO or 0x004C7440
local f = io.open([[D:\AI\gh-remake\lab\ce\dis.txt]], "w")
local n = 0
while a < b and n < 4000 do
  f:write(disassemble(a) .. "\n")
  a = a + getInstructionSize(a)
  n = n + 1
end
f:close()
return n
