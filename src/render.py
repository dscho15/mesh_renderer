import os
import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
from transforms import transform_rpy

cam_pose = trimesh.transformations.rotation_matrix(np.deg2rad(180), [1, 0, 0])

class RenderMesh:

    def __init__(self,
                 mesh,
                 w = 640,
                 h = 480,
                 fov = 74.4845134,
                 znear = 0.001,
                 color = (1., 1., 1.),
                 ambient_light=8
                 ):

        self.fov = np.deg2rad(fov)
        self.h, self.w = h, w
        self.center = mesh.bounding_sphere.primitive.center
        self.diameter = mesh.bounding_sphere.primitive.radius
        
        # scene
        self.scene = pyrender.Scene(bg_color=(255, 0, 0, 0), ambient_light=np.array(color)/ambient_light)
        
        # renderer
        self.renderer = pyrender.OffscreenRenderer(viewport_width=w, viewport_height=h)
        
        # cam
        self.cam = pyrender.PerspectiveCamera(yfov=self.fov, aspectRatio=w/h, znear=znear)
        
        # light
        self.light_h = self.scene.add(pyrender.DirectionalLight(color=color, intensity=15), cam_pose)
        
        # objects
        self.cam_h = self.scene.add(self.cam, pose=cam_pose)
        self.obj_h = self.scene.add(pyrender.Mesh.from_trimesh(mesh, smooth=False))

    def render_obj_pov(self, c_T_obj):
        self.scene.set_pose(self.obj_h, c_T_obj)
        img, _ = self.renderer.render(self.scene, flags=pyrender.RenderFlags.NONE)
        return img

    def render_cam_pov(self, c_T_cam):
        self.scene.set_pose(self.cam_h, c_T_cam)
        self.scene.set_pose(self.light_h, c_T_cam)
        img, _ = self.renderer.render(self.scene, flags=pyrender.RenderFlags.NONE)
        return img

if __name__ == '__main__':
    mesh = trimesh.load_mesh(os.path.dirname(__file__) + "/../data/milk.ply")
    mesh_render = RenderMesh(mesh=mesh)
    img = mesh_render.render_obj_pov(transform_rpy(rpy=[0, 50, 50], p=[0, 0, 0.5]))
    plt.imshow(img)
    plt.show()
