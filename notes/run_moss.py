"""用本机 ComfyUI 的 moss 模型批量出主题装饰底图。

用法：
    python notes/run_moss.py [主题id ...]      # 不传则跑全部

产物：figure/out/decor-<id>.webp（1024 长边，WEBP 质量 82）
"""

import io
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

HOST = "http://127.0.0.1:8188"
WORKFLOW = pathlib.Path(r"C:\Users\doubl\Downloads\moss_deband_int8_api.json")
OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
TMP = pathlib.Path(r"E:\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI\output")

UNET = "moss_image_sft_turbo_int8_convrot.safetensors"
CLIP = "qwen3.5_9b_w4a8_gptq.safetensors"
VAE = "flux2-vae_small.safetensors"

NEGATIVE = (
    "text, watermark, signature, logo, character, face, people, frame, border, "
    "high contrast, busy pattern, noisy, jpeg artifact, worst quality"
)
TAIL = (
    " seamless background texture for a chat app, subtle and low contrast, soft gradients, "
    "no characters, no text, plenty of calm empty space, high detail but restrained"
)

THEMES = {
    "ink": "Traditional Chinese ink wash painting background, pale teal and grey washes, "
    "rice paper grain, drifting mist, a faint bamboo shadow in one corner",
    "maid": "Delicate white lace pattern background, cream and deep navy accents, "
    "tiny ribbon motifs, soft diagonal weave",
    "tech": "Futuristic HUD background, dark teal to navy gradient, thin circuit grid lines, "
    "glowing dots, faint holographic scan lines",
    "sumi": "Minimal sumi-e ink splash on warm rice paper, black ink washes, "
    "one slow brush stroke, enormous white space",
    "moon": "Soft lilac night sky, large pale moon halo, thin drifting clouds, quiet gradient",
    "gyu": "Minimal cream background with soft abstract black cow spots, gentle organic blobs",
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
            outputs = entry.get("outputs", {})
            files = []
            for node in outputs.values():
                for image in node.get("images", []):
                    files.append(image["filename"])
            return files
        time.sleep(3)
    raise TimeoutError(prompt_id)


def build(theme: str, prompt: str, seed: int) -> dict:
    workflow = json.load(io.open(WORKFLOW, encoding="utf-8"))["prompt"]
    workflow["3"]["inputs"]["unet_name"] = UNET
    workflow["4"]["inputs"]["clip_name"] = CLIP
    workflow["5"]["inputs"]["vae_name"] = VAE
    workflow["6"]["inputs"]["value"] = prompt + TAIL
    workflow["8"]["inputs"]["text"] = NEGATIVE
    workflow["14"]["inputs"]["value"] = str(seed)
    # 8 步够用，25 步在 8G 显存上要 offload 很久
    workflow["9"]["inputs"]["expression"] = "8"
    workflow["18"]["inputs"]["filename_prefix"] = f"decor_{theme}"
    return {"prompt": workflow}


def main() -> None:
    targets = sys.argv[1:] or list(THEMES)
    for index, theme in enumerate(targets):
        prompt = THEMES[theme]
        prompt_id = post(build(theme, prompt, 1000 + index))
        print(f"[{theme}] queued {prompt_id}", flush=True)
        files = wait(prompt_id)
        if not files:
            print(f"[{theme}] no output", flush=True)
            continue
        src = TMP / files[0]
        target = OUT / f"decor-{theme}.png"
        target.write_bytes(src.read_bytes())
        print(f"[{theme}] saved {target.name} ({target.stat().st_size // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
