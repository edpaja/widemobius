import pyvista as pv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import argparse
import scienceplots
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

parser = argparse.ArgumentParser(description="Please provide: vtp_folder's path")
## Add arguments for snapshots and run_steps
parser.add_argument("--folderpath", type=str, required=True, help="folder path")
parser.add_argument("--basename", type=str, required=True, help="the basename is the identifying name of the shape. For example, the basename for vertices_N3.inp is 'N3'")

user_args = parser.parse_args()
# Access the parsed arguments
folder_path = user_args.folderpath
basename = user_args.basename

plots = []

#folder_path = '/Users/edouardsavalle/Desktop/University Nots/mebranesimu/examples/01_disclination/MC/'
# Specify the nested directory structure
vtp_path = folder_path+basename+"_vtp_results/"
png_path = folder_path+basename+"_png_results/"

# Create nested directories
try:
    os.makedirs(png_path)
    print(f"Nested directories '{png_path}' created successfully.")
except FileExistsError:
    print(f"One or more directories in '{png_path}' already exist.")
except PermissionError:
    print(f"Permission denied: Unable to create '{png_path}'.")
except Exception as e:
    print(f"An error occurred: {e}")

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

for entry in sorted(os.scandir(vtp_path), key=lambda e: e.name):
        if entry.is_file() and entry.path.endswith('0.vtp'):  # check if it's a file
            print(entry.path)
            #load vtp file
            mesh = pv.read(entry.path)
            #extract points and faces
            points = mesh.points
            faces = mesh.faces.reshape(-1, 4)[:, 1:]  # Assumes triangular faces
            poly3d = [[points[idx] for idx in face] for face in faces]
            collection = Poly3DCollection(poly3d, facecolor='lightblue', edgecolor='k', alpha=0.7)
            plots.append(collection)
            #Create a matplotlib plot
            plt.cla()
            ax.add_collection3d(collection)
            scale = points.flatten()
            ax.auto_scale_xyz(scale, scale, scale)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            entry_name = entry.name
            plt.savefig(png_path+entry_name+".png")


#plt.tight_layout()
#plt.show()