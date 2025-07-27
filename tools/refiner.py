#import pyvista as pv
import pymembrane as mb
import numpy as np
from pprint import pprint
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scienceplots
import os
plt.style.use(['science'])



#N = user_args.N #pentagon size

vertex_file = '/Users/edouardsavalle/Desktop/University Nots/mebranesimu/examples/01_disclination/MC/InputFiles/vertices_N2.inp'
face_file = '/Users/edouardsavalle/Desktop/University Nots/mebranesimu/examples/01_disclination/MC/InputFiles/faces_N2.inp'
vert_pathname, _ = os.path.splitext(vertex_file)
face_pathname, _ = os.path.splitext(face_file)
#basename = os.path.basename(pathname)[9:]
#print(pathname)
#print(basename)

vert_file_path = vert_pathname + "r.inp"
face_file_path = face_pathname + "r.inp"
print(vert_file_path)
print(face_file_path)

try:
    os.mknod(vert_file_path)
    os.mknod(face_file_path)
    print(f"File '{vert_file_path}' and '{face_file_path}' created using os.mknod().")
except OSError as e:
    print(f"Could not create file using os.mknod(): {e}")

#create a system 
box = mb.Box(40.0, 40.0, 40.0)

system = mb.System(box)

#check if the box is loaded correctly
print(system.box)

#read the mesh
system.read_mesh_from_files(files={'vertices':vertex_file, 'faces':face_file})

def midpoint(v1, v2)->tuple:
    x1 = 0.5*(v2.x+v1.x)
    x2 = 0.5*(v2.y+v1.y)
    x3 = 0.5*(v2.z+v1.z)
    return (x1, x2, x3)

def roundcoords(v:list):
    vround=[]
    vround.append(round(v[0],3))
    vround.append(round(v[1],3))
    vround.append(round(v[2],3))
    return vround

verts = system.vertices

vert_index = 0
face_index = 0
all_verts = {} #dictionary where the keys are the vertices and the values are the vertex ids
with open(vert_file_path, "w") as vert_file, open(face_file_path, "w") as face_file:
    face_index = 0
    for f in system.faces:
        v1, v2, v3 = verts[f.v1].r, verts[f.v2].r, verts[f.v3].r
        x = midpoint(v1, v2)
        listv1, listv2, listv3 =(v1.x, v1.y, v1.z), (v2.x, v2.y, v2.z), (v3.x, v3.y, v3.z)
        nv1, nv2, nv3 = midpoint(verts[f.v1].r, verts[f.v2].r), midpoint(verts[f.v2].r, verts[f.v3].r), midpoint(verts[f.v3].r, verts[f.v1].r)
        newverts = [listv1, nv1, listv2, nv2, listv3, nv3]
        face_verts = {listv1:(0,0), nv1:(1,1), listv2:(2,2), nv2:(3,3), listv3:(4,4), nv3:(5,5)}
        face_indices = []
        vert_index = len(all_verts)
        for v in newverts: #cadd new vertices and index 
            if not v in all_verts:
                all_verts.update({v:vert_index})
                face_verts[v] = (face_verts[v][0], vert_index)
                vert_index += 1
            else:
                face_verts[v] = (face_verts[v][0], all_verts[v])
        for pair in face_verts.values():
            face_indices.append(pair[1])
        print(face_verts)
        print(face_indices)
        face1 = f"""{face_index*4}\t{face_indices[0]}\t{face_indices[1]}\t{face_indices[5]}\t1\t1\n"""
        face_file.write(face1)
        print(face1)
        face2 = f"""{face_index*4+1}\t{face_indices[1]}\t{face_indices[3]}\t{face_indices[5]}\t1\t1\n"""
        face_file.write(face2)
        print(face2)
        face3 = f"""{face_index*4+2}\t{face_indices[1]}\t{face_indices[2]}\t{face_indices[3]}\t1\t1\n"""
        face_file.write(face3)
        print(face3)
        face4 = f"""{face_index*4+3}\t{face_indices[5]}\t{face_indices[3]}\t{face_indices[4]}\t1\t1\n"""
        face_file.write(face4)
        print(face4)
        face_index += 1

    for v in all_verts:
        vert_line = f"""{all_verts[v]}\t{v[0]}\t{v[1]}\t{v[2]}\n"""
        vert_file.write(vert_line)
        print(face_verts)
        
        #print(vert)
    

