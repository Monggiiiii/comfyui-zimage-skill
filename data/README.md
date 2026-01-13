# Data Directory

This directory contains character definitions and style guides.

## Files

- `riko_character.py` - Character appearance and outfit definitions
- `style_hojo.md` - Hojo Tsukasa style prompt guide
- `style_satoshi.md` - Satoshi Urushihara style prompt guide
- `__init__.py` - Python package init file

## Customization

### Adding New Outfits

Edit `riko_character.py` and add new entries to the `OUTFITS` dictionary:

```python
OUTFITS = {
    # ... existing outfits ...
    
    "new_outfit": {
        "full": "detailed full body outfit description...",
        "upper": "detailed upper body outfit description..."
    }
}
```

### Creating New Characters

1. Copy `riko_character.py` to a new file (e.g., `new_character.py`)
2. Modify `APPEARANCE` and `OUTFITS` as needed
3. Update the import in generate scripts
