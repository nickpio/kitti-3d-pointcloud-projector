import numpy as np
from pathlib import Path

def load_velodyne_bin(bin_path: str) -> np.ndarray:
    """ Load KITTI .bin point cloud. """
    points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)
    return points

def read_calib_file(calib_path: str) -> dict:
    """ Parse KITTI calib_*.txt -> dict of matrices. """
    calib = {}
    with open(calib_path) as f:
        for line in f:
            key, *vals = line.strip().split()
            if key.endswith(':'):
                key = key[:-1]
                calib[key] = np.array(vals, dtype=np.float32).reshape(3,4) if key.startswith('P') else np.array(vals, dtype=np.float32).reshape(3,3) if key == 'R0_rect' else np.array(vals, dtype=np.float32).reshape(3,4)
            
    # Add homogeneous row for Tr_velo_to_cam
    calib['Tr_velo_to_cam'] = np.vstack((calib['Tr_velo_to_cam'], [0, 0, 0, 1]))
    calib['R0_rect'] = np.vstack((calib['R0_rect'], [0, 0, 0, 1])) # make 4x4
    
    return calib