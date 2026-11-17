-- Select the first row of the "following opcodes write to" window so its details pane fills in. Returns component names.
local s = ""
for i = 0, getFormCount() - 1 do
  local f = getForm(i)
  if f.Caption and f.Caption:find("opcodes") then
    EP03_FOUND = f
    for j = 0, f.ComponentCount - 1 do s = s .. f.Component[j].Name .. ":" .. f.Component[j].ClassName .. " " end
    local lv = f.FoundCodeList or f.foundcodelist
    if lv then
      lv.ItemIndex = 0
      lv.Selected = lv.Items[0]
      if lv.OnSelectItem then pcall(lv.OnSelectItem, lv, lv.Items[0], true) end
    end
  end
end
return s
