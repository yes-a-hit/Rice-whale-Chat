import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 19:05）

### 提示词分层（本轮）

用户澄清：优先级不是二选一，而是**排序拼接**。落地为三层：

1. **system 层**（每轮发）：`resolveSystemPrompt()` = `[systemPrompt, characterPrompt].join('\\n\\n')`，系统提示词在前、角色卡在后，都空才回落官方默认。
2. **辅助层**（只注入一次）：`src/services/chat/promptLayers.ts` 的 `buildAuxBlock()` / `hasAuxInjected()` / `shouldInjectAux()`；`reply.ts` 的 `toRequestMessages()` 在历史里没有 `【规则层】` 标记时，插一对 user/assistant 消息。
3. **历史后指令**：拼在辅助提示词之后，同一对消息里。

预装 `DEFAULT_AUX_PROMPT` = 反鲸八股六条（约 200 字，刻意压短省钱）。
压缩上下文后规则消息被裁掉 → 标记消失 → 下次请求自动重注入（接口已就位，压缩功能本身还没做）。

设置 UI：扩展页新增「启用辅助提示词」开关 + 两个 textarea（辅助提示词带「恢复默认」、历史后指令）。
截图 `notes/aux-ext2.png`。

文档：`docs/prompts.md`（三层结构图、注入判据、为什么这么省、修改位置）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 6.63MB。

### 仍未完成

- 上下文压缩本身（目前只有「压缩后重注入」的判断逻辑）
- 月兔/奶牛/水墨主题立绘
- 本地 NPU 生图与本地 TTS 只有接口
- 真机实测

## 构建
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status + "\n- 调试：`pnpm android:apk`\n- 正式：`pnpm android:release`\n")
print("audit ok")
