#!/usr/bin/env python3
"""
Generate the DS-1 treadle decal from text (reproducible).
Edit the TEXT constants below and re-run to update the decal.
Uses DejaVu fonts (bundled with most Linux, good Unicode coverage).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# --- TEXT CONTENT (edit these to update the decal) ---
# Using U+2B05 (⬅ LEFTWARDS BLACK ARROW) for thicker arrows
TEXT_OUTPUT = "\u2b05 OUTPUT"  # ⬅ OUTPUT (left side, thick arrow)
TEXT_INPUT = "INPUT \u2b05"     # INPUT ⬅ (right side, thick arrow points left)
TEXT_DISTORTION = "Distortion"
TEXT_MODEL = "DS-1"

# --- LAYOUT (positions in 2048x2048 canvas) ---
# Distortion spans full width; DS-1 bottom-right, right-aligned to Distortion's edge
# Spacing: 0.75 gap between INPUT/OUTPUT and Distortion; gap between Distortion and DS-1
POS_OUTPUT = (85, 100)      # top-left
POS_INPUT = (1450, 100)     # top-right
POS_DISTORTION = (100, 400) # middle, spans full width (y=400 for 0.75 space above)
POS_MODEL = (1627, 750)     # bottom-right, right edge aligned (y=750, maintains gap from Distortion)

# --- FONT SIZES ---
SIZE_LABEL = 120    # OUTPUT/INPUT
SIZE_DISTORTION = 391  # Distortion (LiberationSans-Bold, spans full width)
SIZE_MODEL = 140    # DS-1 (LiberationSans-Bold, right-aligned)

# --- COLORS ---
COLOR_BLACK = (0, 0, 0, 255)

def get_font(bold=False, italic=False, size=120, for_arrows=False):
    """Get a font with good Unicode coverage. Uses DejaVu/Liberation.
    
    Args:
        for_arrows: If True, use DejaVuSans-Bold which has U+2B05 (thick arrow).
                   LiberationSans-Bold lacks this glyph.
    """
    # Map to actual available font files
    if for_arrows:
        # Must use DejaVu for thick arrow U+2B05
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    elif bold and italic:
        # For Distortion script - use bold italic serif
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",  # fallback to bold
        ]
    elif bold:
        # Use LiberationSans-Bold (Arial-style) per user pick #2
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
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
    # Labels with arrows use DejaVu (has U+2B05 thick arrow glyph)
    # Distortion and DS-1 use LiberationSans-Bold (user pick #2, Arial-style)
    font_arrow_label = get_font(bold=True, size=SIZE_LABEL, for_arrows=True)
    font_distortion = get_font(bold=True, size=SIZE_DISTORTION)
    font_model = get_font(bold=True, size=SIZE_MODEL)
    
    # Draw text
    # OUTPUT (top-left, arrow points left) - uses DejaVu for arrow glyph
    draw.text(POS_OUTPUT, TEXT_OUTPUT, font=font_arrow_label, fill=COLOR_BLACK)
    
    # INPUT (top-right, arrow points left, on right side of text) - uses DejaVu
    draw.text(POS_INPUT, TEXT_INPUT, font=font_arrow_label, fill=COLOR_BLACK)
    
    # Distortion (middle, LiberationSans-Bold per user pick)
    draw.text(POS_DISTORTION, TEXT_DISTORTION, font=font_distortion, fill=COLOR_BLACK)
    
    # DS-1 (bottom-right, LiberationSans-Bold)
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
