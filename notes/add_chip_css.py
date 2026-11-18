import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\Ext.module.css")
t = io.open(p, encoding="utf-8").read()
if ".modelChips" not in t:
    t += """
.presetBlock {
  margin-bottom: 10px;
}

.modelChips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 6px 0 2px 2px;
}

.modelChip {
  padding: 4px 10px;
  border: 1px solid var(--dsw-alias-border-l1);
  border-radius: 999px;
  background: var(--dsw-alias-bg-base);
  color: var(--dsw-alias-label-secondary);
  font-size: 12.5px;
  cursor: pointer;
}

.modelChipActive {
  border-color: var(--dsw-static-blue-450);
  background: var(--dsw-static-blue-50);
  color: var(--dsw-static-blue-600);
  font-weight: 600;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")
