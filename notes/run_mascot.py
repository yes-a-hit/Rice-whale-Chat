"""用 moss 出各主题的角色立绘（白底、无文字，方便抠图）。

用法：python notes/run_mascot.py [主题id ...]
产物：figure/out/mascot-<id>.png（白底 1024）
"""

import io
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

HOST = "http://127.0.0.1:8188"
WORKFLOW = pathlib.Path(r"E:\flutter\open-deepseek\notes\moss-decor-workflow.json")
OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
TMP = pathlib.Path(r"E:\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI\output")

NEGATIVE = (
    "text, watermark, signature, logo, speech bubble, frame, border, multiple views, "
    "character sheet, extra limbs, bad anatomy, deformed hands, busy background, "
    "photorealistic, 3d render, jpeg artifact, worst quality"
)

BASE = (
    "chibi anime girl character, full body standing, cute, soft cel shading, "
    "clean pure white background, centered composition, high quality illustration"
)

THEMES = {
    "ink": BASE
    + ", traditional Chinese hanfu in pale teal and white, flowing sleeves, "
    "long navy blue hair, whale-like fins on her head, small whale tail, gentle smile, "
    "ink wash inspired coloring",
    "plain": BASE
    + ", simple modern white and soft blue outfit, fitted hoodie and short skirt, "
    "long navy blue hair with a small whale tail, friendly expression, minimal design",
    "sumi": BASE
    + ", monochrome black and grey kimono, sumi-e ink brush style shading, "
    "long black hair, whale tail, calm quiet expression",
    "moon": BASE
    + ", moon rabbit girl, long white-lilac hair, soft rabbit ears with white fur, "
    "pale purple and cream hanfu with moon motifs, tiny bunny tail, dreamy gentle look",
    "gyu": BASE
    + ", cow girl, cream and black spotted patterns, small rounded horns and cow ears, "
    "short black-and-white outfit with a bell, playful smile",
}


def post(payload: dict) -> str:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{HOST}/prompt", data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())["prompt_id"]


def wait(prompt_id: str, timeout: int = 900) -> list[str]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{HOST}/history/{prompt_id}", timeout=15) as response:
                history = json.loads(response.read())
        except urllib.error.URLError:
            time.sleep(2)
            continue
        entry = history.get(prompt_id)
        if entry:
            files = []
            for node in entry.get("outputs", {}).values():
                for image in node.get("images", []):
                    files.append(image["filename"])
            return files
        time.sleep(3)
    raise TimeoutError(prompt_id)


def build(theme: str, prompt: str, seed: int) -> dict:
    workflow = json.load(io.open(WORKFLOW, encoding="utf-8"))["prompt"]
    workflow["6"]["inputs"]["value"] = prompt
    workflow["8"]["inputs"]["text"] = NEGATIVE
    workflow["14"]["inputs"]["value"] = str(seed)
    workflow["9"]["inputs"]["expression"] = "10"
    workflow["15"]["inputs"]["width"] = "832"
    workflow["15"]["inputs"]["height"] = "1216"
    workflow["18"]["inputs"]["filename_prefix"] = f"mascot_{theme}"
    return {"prompt": workflow}


def main() -> None:
    targets = sys.argv[1:] or list(THEMES)
    for index, theme in enumerate(targets):
        prompt_id = post(build(theme, THEMES[theme], 2000 + index))
        print(f"[{theme}] queued {prompt_id}", flush=True)
        files = wait(prompt_id)
        if not files:
            print(f"[{theme}] no output", flush=True)
            continue
        src = TMP / files[0]
        target = OUT / f"mascot-{theme}.png"
        target.write_bytes(src.read_bytes())
        print(f"[{theme}] saved {target.name} ({target.stat().st_size // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
