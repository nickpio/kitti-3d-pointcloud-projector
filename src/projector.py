import numpy as np

def project_point_cloud(pts_velo: np.ndarray, calib: dict, cam: str = 'P2') -> tuple[np.ndarray, np.ndarray]:
    """ 
    Project Velodyne point cloud onto camera image plane.
    Returns (pts_3d_cam, pts_2d_image) for points in front of camera.
    """

    # 1. Homogeneous coordinates 
    # (convert (N, 3) point cloud to (N, 4) by appending column of ones)
    pts_velo_h = np.hstack((pts_velo, np.ones((pts_velo.shape[0], 1))))

    # 2. Velodyne to camera transformation 
    # (Apply intrinsic calibration matrix to transform points from LiDAR to Camera optical frame)
    pts_cam_h = (calib['Tr_velo_to_cam'] @ pts_velo_h.T).T

    # 3. Rectify (R0_rect)
    # (Apply rectification matrix R0_rect to get points in rectified camera coordinate system)
    pts_cam_rect_h = (calib['R0_rect'] @ pts_cam_h.T).T

    # 4. Project (P2)
    # (Apply camera intrinsic + projection matrix P2 to project 3D points to homogeneous image coordinates)
    pts_img_h = (calib[cam] @ pts_cam_rect_h.T).T

    # 5. Normalize and keep only points in front (z > 0)
    # (Divide first 2 columns by third column; converts homogeneous to Cartesian coordinates)
    pts_img = pts_img_h[:, :2] / pts_img_h[:, 2:3]
    # (Create validity mask for points that are in front of the camera, hard coded at KITTI image size)
    mask = (pts_cam_rect_h[:, 2] > 0) & (pts_img[:, 0] >= 0) & (pts_img[:, 0] < 1242) & (pts_img[:, 1] >= 0) & (pts_img[:, 1] < 375)
    
    return pts_cam_rect_h[mask], pts_img[mask]