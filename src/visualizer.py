import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def overlay_points_on_image(img_path: str, pts_2d: np.ndarray, pts_cam: np.ndarray, output_path: str, color_by: str = 'depth'):
    img = Image.open(img_path).convert('RGB')
    fig, ax = plt.subplots(figsize=(12, 4)) # Create figure and single set of axes
    ax.imshow(img) # Display opened image on axes

    # Color by depth, fallback to red if not specified
    if color_by == 'depth':
        ax.scatter(pts_2d[:, 0], pts_2d[:, 1], c=pts_cam[:, 2], cmap='jet_r', s=1.5, alpha=0.7) # Plot 2D points provided by projector
    else:
        ax.scatter(pts_2d[:, 0], pts_2d[:, 1], c='red', s=1.2, alpha=0.7)

    ax.axis('off') # Turn off axes
    plt.savefig(output_path, bbox_inches='tight', dpi=200) # Save figure with tight bounding box and high resolution
    plt.close()