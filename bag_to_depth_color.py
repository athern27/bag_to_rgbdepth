  GNU nano 4.8                                                                                      new3.py                                                                                                
import os
import cv2
import numpy as np
from cv_bridge import CvBridge
from rosbag import Bag

# Paths
rosbag_file = "bagfile.bag"
output_dir = "/outputfolder"#This is absololute path
rgb_topic = "color_image_raw"
depth_topic = "depth_image_raw"

# Create output directories
os.makedirs(f"{output_dir}/rgb_images", exist_ok=True)
os.makedirs(f"{output_dir}/depth_images", exist_ok=True)
os.makedirs(f"{output_dir}/depth_npy", exist_ok=True)

# Initialize CV Bridge
bridge = CvBridge()

# Process the ROS bag
with Bag(rosbag_file, "r") as bag:
    for topic, msg, t in bag.read_messages():
        if topic == rgb_topic:
            # Convert RGB Image
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            timestamp = str(t.to_nsec())
            cv2.imwrite(f"{output_dir}/rgb_images/{timestamp}.png", cv_image)

        elif topic == depth_topic:
            # Convert Depth Image using 'passthrough' encoding for raw depth data
            depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            timestamp = str(t.to_nsec())

            # Optional: Normalize depth image for better visualization (if the values are in mm)
            depth_image = depth_image.astype(np.float32) / 1000.0  # Convert depth from mm to meters
            depth_image = np.uint8(depth_image * 255.0 / np.max(depth_image))  # Normalize to [0, 255]

            # Save depth image as PNG
            cv2.imwrite(f"{output_dir}/depth_images/{timestamp}.png", depth_image)

            # Save depth image as NPY (raw depth data)
            np.save(f"{output_dir}/depth_npy/{timestamp}.npy", depth_image)

print(f"Conversion complete. Files saved in {output_dir}")
