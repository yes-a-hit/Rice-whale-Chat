import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 预装的反鲸八股提示词：短、能省 token、规则可执行
ANTI_SLOP = (
    "写作规则（优先级高于客套）："
    "1. 不用「首先/其次/最后」「综上所述」「总而言之」这类三段式脚手架，直接给结论。"
    "2. 不用「不是…而是…」「不仅…而且」的对偶句凑节奏，一句话说完就停。"
    "3. 少用形容词与副词：不写「深刻地」「极大地」「至关重要」「赋能」「抓手」「闭环」。"
    "4. 不排比、不押韵、不堆破折号；句子长短交错。"
    "5. 具体优先：给数字、给例子、给名字，不写「很多」「各种各样」。"
    "6. 结尾不总结、不喊口号、不反问「你还有什么想了解的」。"
)

p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

if "auxPrompt" not in t:
    t = t.replace(
        "  characterPrompt: string",
        "  characterPrompt: string\n"
        "  /** 辅助提示词（反鲸八股等）：会话首轮注入一次，随后随历史滚动 */\n"
        "  auxPrompt: string\n"
        "  /** 历史后指令：注入在辅助提示词之后，压缩上下文时再次注入 */\n"
        "  tailInstruction: string\n"
        "  /** 是否启用辅助层注入 */\n"
        "  auxEnabled: boolean",
        1,
    )
    t = t.replace(
        "  characterPrompt: 'ods:character-prompt',",
        "  characterPrompt: 'ods:character-prompt',\n"
        "  auxPrompt: 'ods:aux-prompt',\n"
        "  tailInstruction: 'ods:tail-instruction',\n"
        "  auxEnabled: 'ods:aux-enabled',",
        1,
    )
    t = t.replace(
        "  characterPrompt: read(KEYS.characterPrompt) ?? '',",
        "  characterPrompt: read(KEYS.characterPrompt) ?? '',\n"
        "  auxPrompt: read(KEYS.auxPrompt) ?? DEFAULT_AUX_PROMPT,\n"
        "  tailInstruction: read(KEYS.tailInstruction) ?? '',\n"
        "  auxEnabled: read(KEYS.auxEnabled) !== 'false',",
        1,
    )
    t = t.replace(
        "export const DEFAULT_SYSTEM_PROMPT =",
        "export const DEFAULT_AUX_PROMPT = " + repr(ANTI_SLOP).replace("'", "'") + "\n\n"
        "export const DEFAULT_SYSTEM_PROMPT =",
        1,
    )
    t = t.replace(
        "export const setCharacterPrompt =",
        """export const setAuxPrompt = (auxPrompt: string) => {
  write(KEYS.auxPrompt, auxPrompt)
  useSettings.setState({ auxPrompt })
}

export const setTailInstruction = (tailInstruction: string) => {
  write(KEYS.tailInstruction, tailInstruction)
  useSettings.setState({ tailInstruction })
}

export const setAuxEnabled = (auxEnabled: boolean) => {
  write(KEYS.auxEnabled, String(auxEnabled))
  useSettings.setState({ auxEnabled })
}

export const setCharacterPrompt =""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings aux ok")
