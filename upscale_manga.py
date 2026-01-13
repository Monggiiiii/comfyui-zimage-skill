#!/usr/bin/env python3
"""
Manga Style Upscale Script (Hojo/Satoshi)
Uses URL input with LoRA support
"""
import json, urllib.request, urllib.parse, argparse, random, time, os, sys

# ============ CONFIGURATION - MODIFY THESE ============
SERVER = "localhost:8188"  # Your ComfyUI server address
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# ======================================================

# Upscale workflow (with LoRA)
UPSCALE_WORKFLOW = {
    "39": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
    "40": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
    "42": {"inputs": {"conditioning": ["45", 0]}, "class_type": "ConditioningZeroOut"},
    "45": {"inputs": {"text": "", "clip": ["39", 0]}, "class_type": "CLIPTextEncode"},
    "46": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
    "47": {"inputs": {"shift": 3, "model": ["48", 0]}, "class_type": "ModelSamplingAuraFlow"},
    "48": {"inputs": {"lora_name": "", "strength_model": 0.65, "model": ["46", 0]}, "class_type": "LoraLoaderModelOnly"},
    "67": {"inputs": {"filename_prefix": "MangaUpscaled", "images": ["70", 0]}, "class_type": "SaveImage"},
    "70": {
        "inputs": {
            "upscale_by": 1.5, "seed": 0, "steps": 8, "cfg": 1.5, "sampler_name": "euler", "scheduler": "simple",
            "denoise": 0.15, "mode_type": "Linear", "tile_width": 768, "tile_height": 768, "mask_blur": 8,
            "tile_padding": 64, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64,
            "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False,
            "image": ["74", 0], "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0],
            "vae": ["40", 0], "upscale_model": ["71", 0]
        },
        "class_type": "UltimateSDUpscaleCustomSample"
    },
    "71": {"inputs": {"model_name": "4x_MangaJaNai_2048p_V1_ESRGAN_70k.pth"}, "class_type": "UpscaleModelLoader"},
    "74": {"inputs": {"image_url": ""}, "class_type": "LoadImageFromHttpURL"}
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_url", required=True, help="Previously generated image URL")
    parser.add_argument("--lora", required=True, help="LoRA path, e.g., Z-image\\\\z-image-hoko.safetensors")
    parser.add_argument("--prompt", default="", help="Optional: prompt for upscaling")
    parser.add_argument("--upscale_by", type=float, default=1.5, help="Upscale factor")
    args = parser.parse_args()

    wf = json.loads(json.dumps(UPSCALE_WORKFLOW))
    seed = random.randint(0, 10**15)
    
    # Set parameters
    wf["74"]["inputs"]["image_url"] = args.image_url
    wf["48"]["inputs"]["lora_name"] = args.lora
    wf["45"]["inputs"]["text"] = args.prompt
    wf["70"]["inputs"]["seed"] = seed
    wf["70"]["inputs"]["upscale_by"] = args.upscale_by

    try:
        req = urllib.request.Request(
            f"http://{SERVER}/prompt",
            data=json.dumps({"prompt": wf}).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
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
                    "mode": "manga-upscale",
                    "seed": seed
                }))
                return
        print(json.dumps({"status": "error", "error": "timeout"}))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))

if __name__ == "__main__":
    main()
