#!/usr/bin/env python3
"""
Generate the SD-1 treadle decal from text (reproducible).
Based on real Boss SD-1 reference photos (2026-10-01).

Layout (from reference):
- "SUPER" (large, upright bold sans, all caps)
- "OverDrive" (below SUPER, mixed case)
- "SD-1" (right of OverDrive, smaller)
- "<- OUTPUT" (top-left), "INPUT <-" (top-right)
- All BLACK text on transparent (treadle is yellow)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# --- TEXT CONTENT ---
TEXT_OUTPUT = "\u2b05 OUTPUT"  # <- OUTPUT (left side)
TEXT_INPUT = "INPUT \u2b05"     # INPUT <- (right side)
TEXT_SUPER = "SUPER"
TEXT_OVERDRIVE = "OverDrive"
TEXT_MODEL = "SD-1"

# --- LAYOUT (positions in 2048x2048 canvas) ---
# From reference: SUPER top, OverDrive below, SD-1 to the right (no overlap)
POS_OUTPUT = (85, 100)
POS_INPUT = (1450, 100)
POS_SUPER = (100, 350)
POS_OVERDRIVE = (100, 650)
POS_MODEL = (1470, 680)  # tight against OverDrive (ends at x~1439), baseline-aligned

# --- FONT SIZES ---
SIZE_LABEL = 120
SIZE_SUPER = 280       # SUPER - large (965px wide)
SIZE_OVERDRIVE = 280   # OverDrive - same as SUPER (1339px, ends at x=1439)
SIZE_MODEL = 180       # SD-1 - smaller, at x=1550 (no overlap)

# --- COLORS ---
COLOR_BLACK = (0, 0, 0, 255)

def get_font(bold=False, size=120, for_arrows=False):
    if for_arrows:
        candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    elif bold:
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def main():
    img = Image.new('RGBA', (2048, 2048), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font_label = get_font(bold=True, size=SIZE_LABEL, for_arrows=True)
    font_super = get_font(bold=True, size=SIZE_SUPER)
    font_overdrive = get_font(bold=True, size=SIZE_OVERDRIVE)
    font_model = get_font(bold=True, size=SIZE_MODEL)
    
    draw.text(POS_OUTPUT, TEXT_OUTPUT, font=font_label, fill=COLOR_BLACK)
    draw.text(POS_INPUT, TEXT_INPUT, font=font_label, fill=COLOR_BLACK)
    draw.text(POS_SUPER, TEXT_SUPER, font=font_super, fill=COLOR_BLACK)
    draw.text(POS_OVERDRIVE, TEXT_OVERDRIVE, font=font_overdrive, fill=COLOR_BLACK)
    draw.text(POS_MODEL, TEXT_MODEL, font=font_model, fill=COLOR_BLACK)
    
    out = "textures/sd1_treadle_decal.png"
    img.save(out)
    print(f"Saved decal to {out}")
    print(f"  SUPER at {POS_SUPER} (size {SIZE_SUPER})")
    print(f"  OverDrive at {POS_OVERDRIVE} (size {SIZE_OVERDRIVE})")
    print(f"  SD-1 at {POS_MODEL} (size {SIZE_MODEL})")

if __name__ == "__main__":
    main()
