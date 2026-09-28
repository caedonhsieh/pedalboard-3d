#!/usr/bin/env python3
"""
2D projection validator for TS9.
Renders the parametric spec as orthographic top/side views and overlays
on reference photos. No browser, no AI needed.

Usage: python3 tools/render_validate_ts9.py [--write-preview]
"""
import json, math
from PIL import Image, ImageDraw
import numpy as np

SPEC = 'specs/ts9.json'
SIDE_PHOTO = '/home/hatch/workspace/user/media_library/image/57/57ccfa5b5018878a1eb8243c8c5c2d311db55cc3dae415c8e0faceba40824819.png'
TOP_PHOTO = '/tmp/ts9_top_ref.jpg'

def load_spec():
    with open(SPEC) as f:
        return json.load(f)

def render_top_view(spec, scale=200):
    """Orthographic top view: x (width) horizontal, z (depth) vertical.
    Returns PIL image with pedal outline, knobs, footswitch, LED."""
    W, D = spec['dims']['w'], spec['dims']['d']
    w_px, h_px = int(W*scale), int(D*scale)
    img = Image.new('RGB', (w_px+40, h_px+40), (255,255,255))
    d = ImageDraw.Draw(img)
    ox, oy = 20, 20
    
    def px(x, z):
        return ox + (x + W/2)*scale, oy + (z + D/2)*scale
    
    # Pedal outline (rectangle)
    d.rectangle([px(-W/2, -D/2), px(W/2, D/2)], outline=(0,0,0), width=2, fill=(45,140,60))
    
    # Knobs (circles)
    for k in spec.get('knobs', []):
        cx, cy = px(k['x'], k['z'])
        r = 0.175*scale  # measured knob radius
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(30,30,30), outline=(0,0,0))
        # Tick ring
        r2 = 0.28*scale
        for i in range(10):
            a0 = math.radians(i*36)
            a1 = math.radians(i*36+24)
            d.arc([cx-r2, cy-r2, cx+r2, cy+r2], start=math.degrees(a0), end=math.degrees(a1), fill=(0,0,0), width=3)
        # Label
        lx, ly = px(k['x'], k['z']+0.45)
        d.text((lx, ly), k['id'].upper(), fill=(0,0,0), anchor='mm')
    
    # Footswitch
    fs = spec.get('footswitch', {})
    if fs:
        cx, cy = px(fs.get('x', 0), fs.get('z', 1.5))
        r = 0.3*scale
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(40,40,40))
    
    # LED
    led = spec.get('led', {})
    if led:
        cx, cy = px(led.get('x', 0), led.get('z', -2.0))
        r = 0.1*scale
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255,0,0))
    
    return img

def render_side_view(spec, scale=150):
    """Orthographic side view: z (depth) horizontal, y (height) vertical."""
    D, H = spec['dims']['d'], spec['dims']['h']
    pts = spec['enclosure']['points']
    w_px = int(D*scale)+40
    h_px = int(H*scale)+40
    img = Image.new('RGB', (w_px, h_px), (255,255,255))
    d = ImageDraw.Draw(img)
    ox, oy = 20, 20
    
    def px(z, y):
        return ox + (z + D/2)*scale, oy + (H - y)*scale
    
    # Profile polygon (top edge + bottom)
    poly = [px(z, y) for z, y in pts]
    poly.append(px(D/2, 0))
    poly.append(px(-D/2, 0))
    d.polygon(poly, outline=(0,0,0), fill=(45,140,60))
    
    # Knobs (as rectangles on the deck)
    for k in spec.get('knobs', []):
        # Find deck height at knob z
        y_deck = None
        for i in range(len(pts)-1):
            z0, y0 = pts[i]
            z1, y1 = pts[i+1]
            if min(z0,z1) <= k['z'] <= max(z0,z1):
                t = (k['z']-z0)/(z1-z0) if z1!=z0 else 0
                y_deck = y0 + t*(y1-y0)
                break
        if y_deck is None:
            continue
        recess = k.get('recess', 0)
        y_base = y_deck - recess
        y_top = y_base + 0.65
        cx, _ = px(k['z'], 0)
        w = 0.175*scale
        x0, y0p = px(k['z'], y_top)
        x1, y1p = px(k['z'], y_base)
        d.rectangle([cx-w, y0p, cx+w, y1p], fill=(30,30,30), outline=(0,0,0))
    
    return img

def overlay_on_photo(rendered, photo_path, photo_bbox):
    """Overlay rendered image on photo at given bbox. Returns combined image and IoU-like score."""
    photo = Image.open(photo_path).convert('RGB')
    # Resize rendered to fit bbox
    x0, y0, x1, y1 = photo_bbox
    rw, rh = x1-x0, y1-y0
    rend_resized = rendered.resize((rw, rh))
    photo = photo.copy()
    # Blend: 50% opacity overlay
    overlay = Image.new('RGB', photo.size, (255,255,255))
    overlay.paste(rend_resized, (x0, y0))
    combined = Image.blend(photo, overlay, 0.5)
    return combined

if __name__ == '__main__':
    import sys
    spec = load_spec()
    
    # Render views
    top = render_top_view(spec)
    side = render_side_view(spec)
    
    # Save previews
    top.save('/tmp/ts9_top_render.png')
    side.save('/tmp/ts9_side_render.png')
    print("Saved /tmp/ts9_top_render.png and /tmp/ts9_side_render.png")
    
    # Overlay on photos
    # Top photo: pedal bounds from earlier measurement (x=107-1658, y=10-2901)
    top_combined = overlay_on_photo(top, TOP_PHOTO, (107, 10, 1658, 2901))
    top_combined.save('/tmp/ts9_top_overlay.png')
    
    # Side photo: pedal bounds (x=2-746, y=15-306)
    side_combined = overlay_on_photo(side, SIDE_PHOTO, (2, 15, 746, 306))
    side_combined.save('/tmp/ts9_side_overlay.png')
    
    print("Saved overlays to /tmp/ts9_top_overlay.png and /tmp/ts9_side_overlay.png")
    print("\nOpen these to visually verify alignment.")
