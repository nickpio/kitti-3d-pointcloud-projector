from pathlib import Path
from src.kitti_loader import load_velodyne_bin, read_calib_file
from src.projector import project_point_cloud
from src.visualizer import overlay_points_on_image


DATA_ROOT = Path("data/kitti/training")
SAMPLE_IDX = "000002"

velo_path = DATA_ROOT / "velodyne" / f"{SAMPLE_IDX}.bin"
img_path = DATA_ROOT / "image_2" / f"{SAMPLE_IDX}.png"
calib_path = DATA_ROOT / "calib" / f"{SAMPLE_IDX}.txt"

# Load point cloud
pts_velo = load_velodyne_bin(velo_path)

# Load calibration
calib = read_calib_file(calib_path)

# Project point cloud onto image
pts_cam, pts_2d = project_point_cloud(pts_velo, calib, cam='P2')

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
overlay_points_on_image(str(img_path), pts_2d, pts_cam, str(output_dir / f"{SAMPLE_IDX}_projected.png"))

print(f"Projected {len(pts_2d)} points onto outputs/proj_{SAMPLE_IDX}.png")