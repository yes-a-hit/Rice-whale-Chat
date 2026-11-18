# Plus 模式计划（m02997 五条）

> 状态：计划，未开工。

## 1. 可编辑 / 删除回复

**现状**：`AssistantMessage` 有「重新生成」，没有编辑正文，也没有删除单条消息。

**做法**

- 删除：`useChatStore.deleteMessage(sessionId, messageId)`，`MessageList` 的悬浮操作区加垃圾桶。
  删的最后一条若是 assistant，连带把上一轮的 user 一起删掉，避免悬空。
- 编辑：assistant 消息点「编辑」→ 正文变成 textarea → 保存时**只改本地内容，不触发重新生成**
  （主人明确要求这条）。保存后该条 `edited: true`，标题旁标「已编辑」。
- 编辑 user 消息另说：那是「改问题再问」，应该触发重新生成，语义不同，两个按钮分开。

**改哪**：`src/components/messages/AssistantMessage.tsx`、`CommandBar`（操作条）、`store.ts` 加两个 action。
**估时**：4h。

## 2. 每个对话单独配置 agent / 多 agent preset

**现状**：系统提示词、角色卡、模型都是全局单例（`settings.ts`）。

**做法**

- 数据模型：`SessionConfig = { systemPrompt?, characterPrompt?, characterName?, model?, temperature? }`，
  存进 `Session` 记录（IndexedDB v12 迁移，字段可选，缺省回落全局）。
- `resolveSystemPrompt(sessionId)` 改成先读会话级配置、再读全局。
- Preset：`Preset = { id, name, cardId, prompt, model, temperature }`，存在 `ods-presets` store，
  新建会话时可选一个 preset 带入；设置里能建/改/删。
- UI：会话头部一个「⚙ 本对话」弹窗，只暴露五项；preset 在新建对话时选。

**改哪**：`src/services/chat/types.ts`、`store.ts`、`src/services/presets.ts`（新）、
`src/components/session/SessionSettings.tsx`（新）。

**估时**：8h。**前置**：第 3 条的角色卡数据结构要先定。

## 3. 角色卡独立可调 + 绑定背景

**现状**：角色卡只导入不管理，只有一张 `characterPrompt`。

**做法**

- `CharacterCard = { id, name, avatar?, greeting?, prompt, background?, theme? }`，
  存 IndexedDB `ods-cards`。
- 设置里卡片列表：新增 / 编辑 / 删除 / 设为默认。
- 背景：`background` 存一个字面量（`/media/decor-x.webp` 或用户导入的图片 → OPFS），
  绑卡时该会话的 `.frame` 用卡片的背景（优先于主题装饰）。
- 头像：1:1 裁切，显示在消息气泡旁。

**估时**：10h。**依赖**：OPFS 读写（本地导入图片）。

## 4. 对话归档与分类

**做法**

- `Session` 加 `archived: boolean` 与 `tags: string[]`。
- 侧栏加「归档」筛选与标签芯片；长按/右键菜单里「归档」「打标签」。
- 归档的对话不占用主列表，搜索时仍可见（带标记）。

**估时**：5h。改动集中在 `Sider.tsx` 与 `store.ts`。

## 5. 本地数据库 / 知识库工作流

主人原话：「指令导入后进入工作流：清洗 -> 提炼知识 -> 入库 / 点列式浏览 -> RAG」。

这是一整条流水线，拆成四段：

### 5.1 导入与清洗
- 接受 `.md / .txt / .pdf（后做）/ 粘贴`
- 清洗：去页眉页脚、合并断行、去重复段落、保留标题层级
- 输出 `Document { id, title, source, blocks[] }`

### 5.2 提炼知识（LLM 抽取）
- 按块喂给模型（快速档即可），提示词让它输出结构化条目：
  `{ 标题, 要点, 关键词, 原文引用 }`
- 长文档分片 + 并发 2，带进度条（复用 `ModelsSection` 的进度样式）

### 5.3 入库与浏览
- 存储：IndexedDB `ods-knowledge`，条目 + 向量（可选）
- 「点列式浏览」：左侧条目列表，右侧详情（原文引用 + 关键词 + 关联条目）

### 5.4 RAG
- 检索：先做 BM25（纯前端，`minisearch` 之类，约 20KB），够用再做 embedding
- 命中 top-k 后拼进 system prompt 的辅助层（复用 `promptLayers.ts` 的 `buildAuxBlock`）
- 开关放实验页：「知识库检索」

**估时**：5.1 约 4h，5.2 约 5h，5.3 约 6h，5.4 约 6h，合计 ~21h。

**风险**：手机内存与 IndexedDB 容量（大文档 + 向量容易上 GB），需要分页与清理策略。

## 建议顺序

1. 1（可编辑/删除）—— 独立、当天能完
2. 4（归档分类）—— 独立、改动小
3. 3（角色卡）→ 2（preset，依赖角色卡）
4. 5（知识库）—— 最大的，建议单独排期

前三条加起来约 19h，可以分两三天做完；第 5 条视情况再定。
