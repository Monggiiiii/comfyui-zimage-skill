# ComfyUI Z-Image SKILL

> 🎨 An Alma SKILL for generating manga/illustration images via local ComfyUI API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/badge/Twitter-@norsizu-1DA1F2?style=flat&logo=twitter)](https://x.com/norsizu)
[![Civitai](https://img.shields.io/badge/Civitai-norsizu-blue?style=flat)](https://civitai.com/user/norsizu)

## ✨ Features

- **Text-to-Image Generation** via ComfyUI API
- **Multiple Art Styles** with LoRA support:
  - 🖌️ **Hojo Tsukasa** (北条司) - 80s manga style, black & white
  - 🎨 **Satoshi Urushihara** (漆原智志) - 90s anime style, colorful
- **Character Consistency** - Pre-defined character with fixed appearance
- **Quick & High-Res Modes** - Fast preview or production quality
- **Upscaling Support** - Enhance generated images with Ultimate SD Upscale

## 📋 Prerequisites

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) running locally or on a server
- [Alma](https://alma.now/) AI assistant
- [Z-Image](https://github.com/Tongyi-MAI/Z-Image) model: `z_image_turbo_bf16.safetensors`
- Required ComfyUI nodes:
  - `UltimateSDUpscale` (for upscaling)
  - `LoadImageFromHttpURL` (for upscaling from URL)

### Optional LoRA Models

For style transfer, you'll need LoRA models from my Civitai:
- **Hojo Tsukasa Style**: [Download from Civitai](https://civitai.com/models/2298525/zanshou-kin-tsukasa-hojo-style)
- **Satoshi Urushihara Style**: [Download from Civitai](https://civitai.com/models/2287746/zanshou-kin-z-image-satoshi-original-style)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/norsizu/comfyui-zimage-skill.git
```

### 2. Install to Alma skills directory

```bash
# macOS
cp -r comfyui-zimage-skill ~/.config/alma/skills/

# Or create a symlink
ln -s /path/to/comfyui-zimage-skill ~/.config/alma/skills/comfyui-zimage
```

### 3. Configure ComfyUI server address

Edit each Python script and modify the `SERVER` variable:

```python
# ============ CONFIGURATION - MODIFY THESE ============
SERVER = "localhost:8188"  # Your ComfyUI server address
# ======================================================
```

### 4. Configure LoRA paths (if using style transfer)

Update LoRA paths in `SKILL.md` to match your ComfyUI models directory:

```bash
--lora "YOUR_LORA_FOLDER\\z-image-hoko.safetensors"
```

## 📁 Project Structure

```
comfyui-zimage-skill/
├── SKILL.md                    # Main skill document (Alma reads this)
├── generate_riko_quick.py      # Quick generation for Riko character
├── generate_riko_highres.py    # High-res generation for Riko character
├── generate_manga_quick.py     # Quick manga style generation
├── generate_manga_highres.py   # High-res manga style generation
├── upscale_riko.py             # Upscale Riko images (no LoRA)
├── upscale_manga.py            # Upscale manga images (with LoRA)
├── data/
│   ├── riko_character.py       # Character appearance & outfits
│   ├── style_hojo.md           # Hojo style prompt guide
│   ├── style_satoshi.md        # Satoshi style prompt guide
│   └── __init__.py
├── downloads/                  # Generated images saved here
└── README.md
```

## 🎯 Usage

### In Alma Chat

Once installed, simply ask Alma to generate images:

```
"Generate a portrait of a girl in Hojo style"
"Draw Riko in school uniform, looking at cherry blossoms"
"Create a cyberpunk warrior in Satoshi style"
```

### Command Line (Direct)

```bash
# Quick manga generation with Hojo style
python3 generate_manga_quick.py \
  --lora "Z-image\\z-image-hojo.safetensors" \
  --prompt "Zanshou_kin_Hojo, 1girl, solo, office lady, cityscape, monochrome"

# Character generation (Riko)
python3 generate_riko_quick.py \
  --outfit_type school_uniform \
  --scene "standing by window, soft sunlight, peaceful expression"

# High-resolution version
python3 generate_manga_highres.py \
  --lora "Z-image\\z-image-satoshi.safetensors" \
  --prompt "sato, 1girl, fantasy warrior, armor, sunset, shiny skin"
```

## 🎨 Style Comparison

| Feature | Hojo Tsukasa | Satoshi Urushihara |
|---------|--------------|-------------------|
| Era | 80s City Hunter | 90s OVA/Theater |
| Color | Black & White | Full Color |
| Texture | Screentone, ink lines | Glossy skin, reflective |
| Theme | Urban, mature women | Sci-fi, fantasy warriors |
| Trigger | `Zanshou_kin_Hojo` | `sato` |

## 👋 About Me

- **Twitter**: [@norsizu](https://x.com/norsizu)
- **Civitai**: [norsizu](https://civitai.com/user/norsizu)

## 🙏 Acknowledgments

- [Alma](https://alma.now/) by [@yetone](https://twitter.com/yetone) - Amazing AI assistant with SKILL support
- [skill-prompt-generator](https://github.com/huangserva/skill-prompt-generator) by [@huangserva](https://twitter.com/huangserva) - Inspiration for this project
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Powerful and modular Stable Diffusion GUI
- [Z-Image](https://github.com/Tongyi-MAI/Z-Image) - Base model for generation

## 📄 License

MIT License - Feel free to use, modify, and distribute.
