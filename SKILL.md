---
name: comfyui-zimage
description: |
  Z-Image Manga/Illustration Generation. Local scripts, no ToolSearch needed.
  Trigger words: Hojo, Satoshi, manga, generate image, portrait.
---

# Z-Image Image Generation System

**⚠️ Do not use ToolSearch! Run scripts directly with Bash.**

---

## ⚠️ Keyword Understanding (Must Read!)

| User Says | Meaning | Script to Use |
|-----------|---------|---------------|
| high quality, masterpiece, professional | **Good Prompt quality** | `*_quick.py` |
| high-res, upscale, 4K, large image | **High resolution** | `*_highres.py` or `upscale_*.py` |
| default (no specification) | Quick preview | `*_quick.py` |

---

## 🔀 Step 1: Identify Route (Important! Check Priority)

### ⚠️ Route Priority Rules

| Priority | Keyword | Route | Description |
|----------|---------|-------|-------------|
| **1 (Highest)** | Riko | **riko** | Always use riko route when "Riko" is mentioned! |
| 2 | Hojo, Tsukasa Hojo | manga | Pure manga style |
| 3 | Satoshi, Urushihara | manga | Pure manga style |

### Key Understanding

**"Riko in Hojo style" = riko route + Hojo LoRA overlay**

Riko's fixed appearance (hairstyle, facial features) and outfit definitions **only exist in `generate_riko_*.py`**.
If you use `generate_manga_*.py`, you'll lose Riko's characteristics!

### ⚠️ Prompt Extraction Rules When Using Riko

When user requests "Extract prompt from this image, then generate in Riko style":

**Only extract these elements for `--scene` parameter:**
- ✅ Actions, poses (sitting, standing, looking at viewer...)
- ✅ Emotions, expressions (smile, serious, melancholy...)
- ✅ Scene, background (classroom, window, sunset...)
- ✅ Lighting, atmosphere (soft lighting, dramatic shadow...)
- ✅ Composition, angle (close-up, full body, from below...)

**Must discard these elements (Riko has fixed definitions):**
- ❌ Hair color, hairstyle (blonde, ponytail, long hair...)
- ❌ Skin tone (tanned, pale...)
- ❌ Body type (slim, curvy...)
- ❌ Facial features (blue eyes, big eyes...)
- ❌ Clothing (unless user specifies maid instead of school_uniform)

---

## 🎨 Step 2: Execute Generation

```
DIR=/path/to/your/comfyui-zimage-skill
```

### 2.1 Riko Route (Use this whenever Riko is mentioned!)

```bash
# Pure Riko (realistic style)
python3 $DIR/generate_riko_quick.py \
  --outfit_type school_uniform \
  --scene "[scene description]"

# Riko + Hojo style (black and white manga-style Riko)
python3 $DIR/generate_riko_quick.py \
  --outfit_type school_uniform \
  --scene "[scene description]" \
  --lora "Z-image\\z-image-hojo.safetensors" \
  --style_trigger "Zanshou_kin_Hojo, monochrome, greyscale"

# Riko + Satoshi style (90s anime-style Riko)
python3 $DIR/generate_riko_quick.py \
  --outfit_type school_uniform \
  --scene "[scene description]" \
  --lora "Z-image\\z-image-satoshi.safetensors" \
  --style_trigger "sato, 90s anime style" \
  --style_tags "shiny skin, sparkle"
```

**Outfit options**: `school_uniform` (JK uniform) | `maid` (maid outfit)
**View options**: `--view_type full` (full body) | `--view_type upper` (upper body)

### 2.2 Pure Manga Route (When Riko is not involved)

```bash
# Hojo style
python3 $DIR/generate_manga_quick.py \
  --lora "Z-image\\z-image-hojo.safetensors" \
  --prompt "[full prompt]"

# Satoshi style
python3 $DIR/generate_manga_quick.py \
  --lora "Z-image\\z-image-satoshi.safetensors" \
  --prompt "[full prompt]"
```

### 2.3 High-Resolution Version (When user explicitly requests "high-res")

Replace `*_quick.py` with `*_highres.py`, requires `timeout=300000`

---

## 📤 Step 3: Display Results

```html
<a href="[image_url]"><img src="[image_url]" width="350"></a>
```

**Save image_url for later upscaling!**

---

## 🔍 Step 4: Upscale Existing Images

When user says "upscale" for an already generated image:

```bash
# Riko image upscale (no LoRA needed)
python3 $DIR/upscale_riko.py --image_url "[image_url]"

# Manga image upscale (needs original LoRA)
python3 $DIR/upscale_manga.py --image_url "[image_url]" --lora "[original LoRA]"
```

---

## 📋 Quick Decision Table

| User Request | Route | Script | LoRA |
|--------------|-------|--------|------|
| Draw Riko | riko | `generate_riko_quick.py` | None |
| Riko in Hojo style | **riko** | `generate_riko_quick.py` | hojo + style_trigger |
| Riko in Satoshi style | **riko** | `generate_riko_quick.py` | satoshi + style_trigger |
| Mecha girl in Hojo style | manga | `generate_manga_quick.py` | hojo |
| Cyberpunk in Satoshi style | manga | `generate_manga_quick.py` | satoshi |

---

## ⚠️ Notes

1. **Riko first** — Always use riko route when "Riko" is mentioned
2. **LoRA path uses double backslash** `\\`
3. **highres/upscale needs** `timeout=300000`
4. **Style guides are in data/** — Do not delete
