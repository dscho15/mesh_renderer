import trimesh
import numpy as np

x_axis, y_axis, z_axis = [1, 0, 0], [0, 1, 0], [0, 0, 1]


def transform_rpy(rpy=np.array([0, 0, 0]), p=np.array([0, 0, 0])):
    r_x = trimesh.transformations.rotation_matrix(np.deg2rad(rpy[0]), x_axis)
    r_y = trimesh.transformations.rotation_matrix(np.deg2rad(rpy[1]), y_axis)
    r_z = trimesh.transformations.rotation_matrix(np.deg2rad(rpy[2]), z_axis)
    rpy = trimesh.transformations.concatenate_matrices(r_x, r_y, r_z)
    rpy[:3, 3] = np.array(p)
    return rpy
