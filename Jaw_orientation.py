# Jaw Orientation
# Import Required Packages
import vedo
import numpy as np
import os

# Get name from path
def get_file_name_from_path(file_path):
    """
    Function to extract the file name from a given path

    Input: directory
    Output: file name
    """
    return os.path.basename(file_path)

def identify_mesh_file(file_name, mesh):
    """
    Function to adjust the mesh orientation based on the file name

    Input: file name, mesh
    Output: Mesh with the required orientation
    """
    if "upper" in file_name.lower():
        print("This is an upper jaw and must be inverted")
        return mesh.mirror('z')
    elif "lower" in file_name.lower():
        print("This is an lower jaw, no changes needed")
        return mesh
    return mesh

def identify_jaw_orientation(file_path, mesh):
    '''
    Function to determine and adjust the mesh orientation using the file name

    Input: file name, mesh
    Output: Mesh with the required orientation
    '''
    # 1. Determine file name
    file_name = get_file_name_from_path(file_path)

    # Determine mesh orientation
    new_mesh = identify_mesh_file(file_name, mesh)

    return new_mesh


