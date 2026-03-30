# TODO: Add Path usage
# TODO: Add basic validation

import numpy as np
from pathlib import Path

def load_velodyne_bin(bin_path: str) -> np.ndarray:
    """ Load KITTI .bin point cloud. """
    points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)
    return points[:, :3] # Only return x, y, z for basic projection, intensity is ignored

def read_calib_file(calib_path: str) -> dict:
    """ Parse KITTI calib_*.txt -> dict of matrices. """
    calib = {}
    with open(calib_path) as f:
        for line in f:
            line = line.strip()
            if not line:  # skip empty or whitespace-only lines
                continue
            # Split on first ':' 
            if ':' not in line:
                continue  # safety
            key_part, value_part = line.split(':', 1)
            key = key_part.strip()
            # Get numbers only
            vals = [float(x) for x in value_part.strip().split() if x]
            if not vals:
                continue

            if key in ['P0', 'P1', 'P2', 'P3']:
                calib[key] = np.array(vals, dtype=np.float32).reshape(3, 4)
            elif key == 'R0_rect':
                calib[key] = np.array(vals, dtype=np.float32).reshape(3, 3)
            elif key in ['Tr_velo_to_cam', 'Tr_imu_to_velo']:
                calib[key] = np.array(vals, dtype=np.float32).reshape(3, 4)
            # Ignore others like Tr_cam_to_road if present

    # Make homogeneous versions (required for projection math)
    if 'Tr_velo_to_cam' in calib:
        Tr = np.eye(4, dtype=np.float32)
        Tr[:3, :4] = calib['Tr_velo_to_cam']
        calib['Tr_velo_to_cam'] = Tr

    if 'R0_rect' in calib:
        R0 = np.eye(4, dtype=np.float32)
        R0[:3, :3] = calib['R0_rect']
        calib['R0_rect'] = R0

    return calib