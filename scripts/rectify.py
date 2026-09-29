#!/usr/bin/env python3
"""
Photo rectification via homography.
Maps reference photos to true orthographic views using known dimensions.
"""

import numpy as np
from PIL import Image
from scipy import ndimage
from pathlib import Path

def find_corners(mask):
    """
    Find the 4 corners of a quadrilateral mask.
    Uses the convex hull and approximates to 4 points.
    Returns corners in order: [top-left, top-right, bottom-right, bottom-left].
    """
    ys, xs = np.where(mask)
    points = np.stack([xs, ys], axis=1).astype(np.float32)

    # Convex hull via scipy
    from scipy.spatial import ConvexHull
    try:
        hull = ConvexHull(points)
        hull_pts = points[hull.vertices]
    except:
        # Fallback: use bounding box corners
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], dtype=np.float32)

    # Approximate hull to 4 corners using the extreme points
    # Find the 4 points that are most "corner-like"
    # Method: for each hull point, compute angle; keep the 4 with sharpest angles
    # Simpler: use the bounding box of the hull and find closest hull points to corners

    x0, x1 = hull_pts[:, 0].min(), hull_pts[:, 0].max()
    y0, y1 = hull_pts[:, 1].min(), hull_pts[:, 1].max()

    # Target corners in image coords
    targets = np.array([
        [x0, y0],  # top-left
        [x1, y0],  # top-right
        [x1, y1],  # bottom-right
        [x0, y1],  # bottom-left
    ], dtype=np.float32)

    # For each target, find the closest hull point
    corners = []
    for tx, ty in targets:
        dists = np.sqrt((hull_pts[:, 0] - tx)**2 + (hull_pts[:, 1] - ty)**2)
        corners.append(hull_pts[np.argmin(dists)])

    return np.array(corners, dtype=np.float32)

def compute_homography(src_pts, dst_pts):
    """
    Compute 3x3 homography matrix mapping src_pts to dst_pts.
    src_pts, dst_pts: (4, 2) arrays.
    """
    # Direct Linear Transform (DLT)
    A = []
    for (x, y), (xp, yp) in zip(src_pts, dst_pts):
        A.append([-x, -y, -1, 0, 0, 0, x*xp, y*xp, xp])
        A.append([0, 0, 0, -x, -y, -1, x*yp, y*yp, yp])
    A = np.array(A)
    _, _, Vt = np.linalg.svd(A)
    H = Vt[-1].reshape(3, 3)
    return H / H[2, 2]

def warp_perspective(img, H, output_size):
    """
    Warp image using homography.
    img: PIL Image. H: 3x3 homography (src to dst). output_size: (w, h).
    """
    # Invert for backward mapping
    H_inv = np.linalg.inv(H)

    w, h = output_size
    # Create coordinate grids
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # Apply inverse homography
    src_x = (H_inv[0,0]*xx + H_inv[0,1]*yy + H_inv[0,2]) / \
            (H_inv[2,0]*xx + H_inv[2,1]*yy + H_inv[2,2])
    src_y = (H_inv[1,0]*xx + H_inv[1,1]*yy + H_inv[1,2]) / \
            (H_inv[2,0]*xx + H_inv[2,1]*yy + H_inv[2,2])

    # Sample using PIL (convert to numpy, use map_coordinates, convert back)
    arr = np.array(img)
    from scipy.ndimage import map_coordinates

    warped = np.zeros((h, w, arr.shape[2]), dtype=arr.dtype)
    for c in range(arr.shape[2]):
        warped[:,:,c] = map_coordinates(
            arr[:,:,c], [src_y, src_x], order=1, mode='constant', cval=0
        )

    return Image.fromarray(warped)

def rectify_top_homography(photo_path, output_px_per_in=200):
    """
    Rectify top photo to orthographic using homography.
    Target: 2.91" (w) x 4.88" (d).
    Returns (rectified PIL Image, px_per_in).
    """
    img = Image.open(photo_path).convert('RGB')
    arr = np.array(img).astype(float)

    # Segment green body
    g, r, b = arr[:,:,1], arr[:,:,0], arr[:,:,2]
    green_mask = (g > 100) & (g > r + 10) & (r < 160)
    labeled, n = ndimage.label(green_mask)
    sizes = np.array([(labeled == i).sum() for i in range(1, n+1)])
    body = (labeled == (np.argmax(sizes) + 1))
    body = ndimage.binary_fill_holes(body)

    # Find corners
    corners = find_corners(body)
    # corners: [top-left, top-right, bottom-right, bottom-left]
    # In the photo: top = back of pedal (-z), bottom = front (+z)
    #               left = -x, right = +x

    # Destination: rectangle with correct aspect
    # Width (x): 2.91", Height (y/image): 4.88"
    px_per_in = output_px_per_in
    dst_w = int(2.91 * px_per_in)
    dst_h = int(4.88 * px_per_in)
    dst_corners = np.array([
        [0, 0],
        [dst_w, 0],
        [dst_w, dst_h],
        [0, dst_h],
    ], dtype=np.float32)

    H = compute_homography(corners, dst_corners)
    rectified = warp_perspective(img, H, (dst_w, dst_h))

    return rectified, px_per_in

def rectify_side_homography(photo_path, output_px_per_in=200):
    """
    Rectify side photo to orthographic using homography.
    Target: 4.88" (d, horizontal) x 2.09" (h, vertical).
    Returns (rectified PIL Image, px_per_in).
    """
    img = Image.open(photo_path).convert('RGB')
    arr = np.array(img).astype(float)

    # Segment green housing
    g, r, b = arr[:,:,1], arr[:,:,0], arr[:,:,2]
    green_mask = (g > 100) & (g > r + 20) & (g > b - 10) & (r < 150)
    labeled, n = ndimage.label(green_mask)
    sizes = np.array([(labeled == i).sum() for i in range(1, n+1)])
    housing = (labeled == (np.argmax(sizes) + 1))
    housing = ndimage.binary_fill_holes(housing)

    # Find corners
    corners = find_corners(housing)
    # In the side photo: left = back (-z), right = front (+z)
    #                   top = up (+y), bottom = down (0)

    px_per_in = output_px_per_in
    dst_w = int(4.88 * px_per_in)  # depth (horizontal)
    dst_h = int(2.09 * px_per_in)  # height (vertical)
    dst_corners = np.array([
        [0, 0],
        [dst_w, 0],
        [dst_w, dst_h],
        [0, dst_h],
    ], dtype=np.float32)

    H = compute_homography(corners, dst_corners)
    rectified = warp_perspective(img, H, (dst_w, dst_h))

    return rectified, px_per_in
