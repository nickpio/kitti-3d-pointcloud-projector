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
            key, *vals = line.strip().split() # Remove whitespace and split into tokens, take first token as key
            if key.endswith(':'): # Normalize key
                key = key[:-1]

            # If key starts with 'P', it is a projection matrix, reshape to 3x4
            # If key is 'R0_rect', it is a rotation (rectification) matrix, reshape to 3x3
            # If key is 'Tr_velo_to_cam', it is a transformation (LiDAR to Camera 0) matrix, reshape to 3x4
            arr = np.array(vals, dtype=np.float32)
            if key.startswith('P'):
                calib[key] = arr.reshape(3, 4)
            elif key == 'R0_rect':
                calib[key] = arr.reshape(3, 3)
            else:
                calib[key] = arr.reshape(3, 4)
            
    # Add homogeneous row for Tr_velo_to_cam
    calib['Tr_velo_to_cam'] = np.vstack((calib['Tr_velo_to_cam'], [0, 0, 0, 1]))
    calib['R0_rect'] = np.vstack((calib['R0_rect'], [0, 0, 0, 1])) # make 4x4

    return calib