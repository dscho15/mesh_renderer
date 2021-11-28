import os
import trimesh
import numpy as np
import matplotlib.pyplot as plt
import cv2
import json
from tqdm import tqdm

from transforms import transform_rpy
from render import RenderMesh
from create_poses import CameraPoseSphere

os.environ['PYOPENGL_PLATFORM'] = 'egl'

cam_opengl_to_cv = trimesh.transformations.rotation_matrix(np.deg2rad(180), [1, 0, 0])

if __name__ == '__main__':
    
    # settings should be located in data
    with open(os.path.dirname(__file__) + '/../data/settings.json', 'r') as read_file:
        # load the settings
        settings = json.load(read_file)
        lat_begin = settings["lat_begin"]
        lat_end = settings["lat_end"]
        lon_begin = settings["lon_begin"]
        lon_end = settings["lon_end"]
        subdivisions = settings["subdivisions"]
        replace_prev_templates = settings["replace_prev_templates"]
        path2templates = settings["path2temp"]
        path2mesh = settings["path2mesh"]
        north_pole = settings["north_pole"]
        radius = settings["radius"]
        visualize_frames = settings["visualize_frames"]
        width = settings["img_width"]
        height = settings["img_height"]
        z_near = settings["z_near"]
        fov = settings["fov"]
        z_near = settings["z_near"]
    
    path = os.path.dirname(__file__) + path2templates
    
    if replace_prev_templates:
        [os.remove(path+file) for file in os.listdir(path) if file.endswith('.jpg') or file.endswith('.txt')]
    
    mesh = trimesh.load_mesh(os.path.dirname(__file__) + path2mesh)
    
    rm = RenderMesh(mesh, width, height, fov, z_near)
    
    cps = CameraPoseSphere(lat_begin, 
                           lat_end, 
                           lon_begin, 
                           lon_end,
                           north_pole,
                           subdivisions=subdivisions)
    
    R, T = cps.generate_cam_frames(mesh.bounding_box.centroid, radius, visualize_frames, mesh)
    
    for i in tqdm(range(T.shape[0])):
        
        cam_pose = np.identity(4)
        cam_pose[:3, :3] = R[i, :, :]
        cam_pose[:3,  3] = T[i]

        # render image from camera angle
        img = rm.render_cam_pov(cam_pose @ cam_opengl_to_cv)
        
        # write to template folder
        cv2.imwrite(os.path.join(path, 'template' + str(i).zfill(4) + '.jpg'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        
        # write the pose to folder
        np.savetxt(os.path.join(path, 'template' + str(i).zfill(4) + '_pose.txt'), cam_pose, delimiter = ', ', fmt='%.8f')