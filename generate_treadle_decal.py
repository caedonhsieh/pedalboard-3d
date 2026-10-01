#!/usr/bin/env python3
"""
Generate the DS-1 treadle decal from text (reproducible).
Edit the TEXT constants below and re-run to update the decal.
Uses DejaVu fonts (bundled with most Linux, good Unicode coverage).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# --- TEXT CONTENT (edit these to update the decal) ---
TEXT_OUTPUT = "\u2190 OUTPUT"  # ← OUTPUT (left side)
TEXT_INPUT = "INPUT \u2190"     # INPUT ← (right side, arrow points left)
TEXT_DISTORTION = "Distortion"
TEXT_MODEL = "DS-1"

# --- LAYOUT (positions in 2048x2048 canvas) ---
# These match the original traced decal layout
POS_OUTPUT = (85, 100)      # top-left
POS_INPUT = (1450, 100)     # top-right
POS_DISTORTION = (250, 300) # middle, large script
POS_MODEL = (1250, 650)     # bottom-right

# --- FONT SIZES ---
SIZE_LABEL = 120    # OUTPUT/INPUT
SIZE_DISTORTION = 280  # Distortion script
SIZE_MODEL = 140    # DS-1

# --- COLORS ---
COLOR_BLACK = (0, 0, 0, 255)

def get_font(bold=False, italic=False, size=120):
    """Get a font with good Unicode coverage. Uses DejaVu/Liberation."""
    # Map to actual available font files
    if bold and italic:
        # For Distortion script - use bold italic serif
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",  # fallback to bold
        ]
    elif bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
    elif italic:
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    
    print(f"Warning: Could not find font, using default")
    return ImageFont.load_default()

def main():
    # Create 2048x2048 transparent canvas
    img = Image.new('RGBA', (2048, 2048), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    font_label = get_font(bold=True, size=SIZE_LABEL)
    font_distortion = get_font(bold=True, italic=True, size=SIZE_DISTORTION)
    font_model = get_font(bold=True, size=SIZE_MODEL)
    
    # Draw text
    # OUTPUT (top-left, arrow points left)
    draw.text(POS_OUTPUT, TEXT_OUTPUT, font=font_label, fill=COLOR_BLACK)
    
    # INPUT (top-right, arrow points left, on right side of text)
    draw.text(POS_INPUT, TEXT_INPUT, font=font_label, fill=COLOR_BLACK)
    
    # Distortion (middle, italic serif)
    draw.text(POS_DISTORTION, TEXT_DISTORTION, font=font_distortion, fill=COLOR_BLACK)
    
    # DS-1 (bottom-right, bold)
    draw.text(POS_MODEL, TEXT_MODEL, font=font_model, fill=COLOR_BLACK)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), 'textures', 'ds1_treadle_decal.png')
    img.save(output_path)
    print(f"Saved decal to {output_path}")
    print(f"  OUTPUT: '{TEXT_OUTPUT}' at {POS_OUTPUT}")
    print(f"  INPUT: '{TEXT_INPUT}' at {POS_INPUT}")
    print(f"  Distortion at {POS_DISTORTION}")
    print(f"  DS-1 at {POS_MODEL}")

if __name__ == '__main__':
    main()
