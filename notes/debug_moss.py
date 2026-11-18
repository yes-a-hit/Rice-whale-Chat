import io
import json
import pathlib
import urllib.error
import urllib.request

HOST = "http://127.0.0.1:8188"
WORKFLOW = pathlib.Path(r"C:\Users\doubl\Downloads\moss_deband_int8_api.json")

workflow = json.load(io.open(WORKFLOW, encoding="utf-8"))["prompt"]
workflow["3"]["inputs"]["unet_name"] = "moss_image_sft_turbo_int8_convrot.safetensors"
workflow["4"]["inputs"]["clip_name"] = "qwen3.5_9b_w4a8_gptq.safetensors"
workflow["5"]["inputs"]["vae_name"] = "flux2-vae_small.safetensors"

data = json.dumps({"prompt": workflow}).encode("utf-8")
request = urllib.request.Request(
    f"{HOST}/prompt", data=data, headers={"Content-Type": "application/json"}
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        print(response.read().decode())
except urllib.error.HTTPError as error:
    print("status", error.code)
    print(error.read().decode()[:2000])
