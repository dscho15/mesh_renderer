from typing import List
import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def normalize(arr):
    arr_sqrd = np.sqrt(np.sum(arr * arr, axis = 1))
    for i in range(3):
        arr[:, i] *= 1/arr_sqrd
    return arr

class CameraPoseSphere:

    def __init__(self,
                 lat_begin=0.,
                 lat_end=360.,
                 lon_begin=0.,
                 lon_end=90.,
                 north_pole=[0., 0., 1.],
                 subdivisions=2
                 ):
        # settings
        self.lat_begin = np.deg2rad(lat_begin)
        self.lat_end = np.deg2rad(lat_end)
        self.lon_begin = np.deg2rad(lon_begin)
        self.lon_end = np.deg2rad(lon_end)
        self.north_pole = np.array(north_pole) / np.linalg.norm(north_pole)
        # gen verticies of a icosphere
        icosphere = np.array(trimesh.creation.icosphere(subdivisions, 1).vertices)
        # we mask by lat/longtitude
        icosphere_pow = icosphere * icosphere
        r = icosphere_pow[:, 0] + icosphere_pow[:, 1]
        lat = np.arctan2(icosphere[:, 1], icosphere[:, 0])
        lat[lat < 0] += 2*np.pi
        lon = np.abs(np.arctan2(icosphere[:, 2], np.sqrt(r)) - np.pi/2)
        # mask
        mask = (self.lat_begin <= lat) & (lat <= self.lat_end) & (self.lon_begin <= lon) & (lon <= self.lon_end)
        # only keep the ones that are needed
        self.vertices = icosphere[mask]

    def generate_cam_frames(self, centroid: List, radius: List, vis = False, mesh = None):
        
        centroid, radius = np.r_[centroid], np.r_[radius]
        
        # store
        R_, T_ = [], []
        
        for r in radius:
        
            # column 3 of the rotation matrix
            R = np.zeros((self.vertices.shape[0], 3, 3))
            R[:, :, 2] = -self.vertices
            mask_not_north = ~(abs(np.sum(R[:, :, 2] * self.north_pole, axis = 1)) > 1-1e-5)
            
            # scale the vertices - hence they are unit - with the centroid and user defined radius
            T = r * self.vertices.copy() + centroid
            
            # north pole
            cam_north_pole_dir = normalize(r * self.north_pole - T)
            
            # column 2 of the rotation matrix
            # the north pole of the camera is used to define the negative y-axis by projecting onto the image plane via. third column of R
            for i in range(3):
                R[mask_not_north, i, 1] = cam_north_pole_dir[mask_not_north, i] - np.sum(cam_north_pole_dir[mask_not_north, :] * R[mask_not_north, :, 2], axis = 1)  * R[mask_not_north, i, 2]
            R[mask_not_north, :, 1] = -normalize(R[mask_not_north, :, 1])
            
            # parallel mask, simply define it was the following
            R[~mask_not_north, :, 1] = np.array([0, 1, 0])
            
            # compute column 1 of the rotation matrix
            R[:, :, 0] = normalize(np.cross(R[:, :, 1], R[:, :, 2]))
            
            R_.append(R); T_.append(T);
        
        # stack frames
        T, R = np.vstack(T_), np.vstack(R_)
        
        # if visualize
        if vis is True:
            
            fig = plt.figure(figsize=(7, 7))
            ax = fig.add_subplot(projection='3d')
            
            if mesh is not None:
                ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2])
            else:
                ax.scatter(centroid[0], centroid[1], centroid[2], marker='x')
            
            for i in range(T.shape[0]):
            
                # compute pts for plot
                Tx = T[i] + R[i] @ np.array([0.1, 0, 0])
                Ty = T[i] + R[i] @ np.array([0, 0.1, 0])
                Tz = T[i] + R[i] @ np.array([0, 0, 0.1])
            
                # plot 3d
                ax.plot3D([T[i][0], Tx[0]], [T[i][1], Tx[1]], [T[i][2], Tx[2]], color='red') # x
                ax.plot3D([T[i][0], Ty[0]], [T[i][1], Ty[1]], [T[i][2], Ty[2]], color='green') # y
                ax.plot3D([T[i][0], Tz[0]], [T[i][1], Tz[1]], [T[i][2], Tz[2]], color='blue') # z
            
            ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
            ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2, 2);
            
            plt.grid()
            plt.show()
        
        return R, T
    
    def plot_vertices(self):
        
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(projection='3d')
        
        ax.scatter(self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2])
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2, 2);
        
        plt.grid()
        plt.show()
    
if __name__ == '__main__':
    
    mesh = trimesh.load_mesh(os.path.dirname(__file__) + "/../data/milk.ply")
    cam_sphere = CameraPoseSphere()
    cam_sphere.generate_cam_frames(mesh.bounding_box.centroid, [1], mesh=mesh, vis=True)