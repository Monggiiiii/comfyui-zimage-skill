#!/usr/bin/env python3
"""
Manga Style High-Resolution Generation Script
Higher quality output with more steps and larger resolution
"""
import json, urllib.request, urllib.parse, argparse, sys, random, time, os

# ============ CONFIGURATION - MODIFY THESE ============
SERVER = "localhost:8188"  # Your ComfyUI server address
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# ======================================================

# High-res workflow: More steps, higher quality
HIGHRES_WORKFLOW = {
    "39": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
    "40": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
    "42": {"inputs": {"conditioning": ["45", 0]}, "class_type": "ConditioningZeroOut"},
    "44": {
        "inputs": {
            "seed": 0, "steps": 20, "cfg": 1.5, "sampler_name": "euler", "scheduler": "simple",
            "denoise": 1, "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["64", 0]
        },
        "class_type": "KSampler"
    },
    "45": {"inputs": {"text": "", "clip": ["39", 0]}, "class_type": "CLIPTextEncode"},
    "46": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
    "47": {"inputs": {"shift": 3, "model": ["48", 0]}, "class_type": "ModelSamplingAuraFlow"},
    "48": {"inputs": {"lora_name": "", "strength_model": 0.65, "model": ["46", 0]}, "class_type": "LoraLoaderModelOnly"},
    "64": {"inputs": {"width": 1536, "height": 2048, "batch_size": 1}, "class_type": "EmptyLatentImage"},
    "67": {"inputs": {"filename_prefix": "HighRes", "images": ["43", 0]}, "class_type": "SaveImage"},
    "43": {"inputs": {"samples": ["44", 0], "vae": ["40", 0]}, "class_type": "VAEDecode"}
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--lora", required=True)
    parser.add_argument("--width", type=int, default=1536)
    parser.add_argument("--height", type=int, default=2048)
    args = parser.parse_args()

    # --- Monochrome Enforcement for Hojo Style ---
    final_prompt = args.prompt
    lora_lower = args.lora.lower()
    prompt_lower = args.prompt.lower()
    
    if "hoko" in lora_lower or "hojo" in prompt_lower:
        final_prompt = "(monochrome:1.5), (greyscale:1.5), (black and white:1.4), (black and white manga:1.3), no color, manga style, high contrast, " + args.prompt + ", monochrome, greyscale"

    wf = json.loads(json.dumps(HIGHRES_WORKFLOW))
    seed = random.randint(0, 10**15)
    wf["45"]["inputs"]["text"] = final_prompt
    wf["48"]["inputs"]["lora_name"] = args.lora
    wf["64"]["inputs"]["width"] = args.width
    wf["64"]["inputs"]["height"] = args.height
    wf["44"]["inputs"]["seed"] = seed

    try:
        req = urllib.request.Request(f"http://{SERVER}/prompt", data=json.dumps({"prompt": wf}).encode('utf-8'), headers={"Content-Type": "application/json"})
        prompt_id = json.loads(urllib.request.urlopen(req).read())['prompt_id']
        
        for _ in range(180):  # 3 minutes timeout
            time.sleep(1)
            history = json.loads(urllib.request.urlopen(f"http://{SERVER}/history/{prompt_id}").read())
            if prompt_id in history:
                img = history[prompt_id]['outputs']['67']['images'][0]
                url = f"http://{SERVER}/view?{urllib.parse.urlencode({'filename': img['filename'], 'subfolder': '', 'type': 'output', 't': int(time.time()*1000)})}"
                
                # Download to local
                save_dir = os.path.join(SKILL_DIR, "downloads")
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, img['filename'])
                try:
                    urllib.request.urlretrieve(url, save_path)
                except Exception as e:
                    print(f"Download failed: {e}", file=sys.stderr)

                print(json.dumps({
                    "status": "success", 
                    "image_url": url, 
                    "filename": img['filename'],
                    "mode": "highres", 
                    "seed": seed
                }))
                return
        print(json.dumps({"status": "error", "error": "timeout"}))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))

if __name__ == "__main__":
    main()
