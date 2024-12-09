# Main. Execute all functions.
# Import required packages
import vedo
import numpy as np
import os
# import time
import matplotlib.pyplot as plt
from Jaw_orientation import identify_jaw_orientation
from Occlusal_plane_aprox_algorithm import occlusal_plane_algorithm, get_plane_information
from Grid_splitting_algorithm import determine_high_point_and_grid_cells
from Cutting_algorithm import cutting_algorithm

# File path
file_path = "C:/Program Files/Dental_data/Data/PiB_01_20241007094638_UpperJaw.stl"

def remove_soft_tissue(file_path, cell_size, inclusion_criterion, distance_threshold_ratio):
    '''
    Function to remove soft tissue

    Input: file_path, cell_size, inclusion_criterion, distance_threshold_ratio
    Output: cleaned mesh (vedo object)
    '''
    #start_time = time.time()

    # Step 1: Transform file into mesh and get information
    mesh = vedo.Mesh(file_path)
    # mesh = mesh.decimate(fraction=0.03)

    print(file_path)

    # Step 1.1: Compute global variables
    global points
    points = mesh.vertices
    global center_of_mass
    center_of_mass = mesh.center_of_mass()
    global bounds
    bounds = mesh.bounds()  # [xmin, xmax, ymin, ymax, zmin, zmax]

    # Step 2: Determine orientation and change if necessary
    inverted_mesh = identify_jaw_orientation(file_path, mesh)

    # Step 3: Approximate the occlusal plane
    occlusal_plane = occlusal_plane_algorithm(inverted_mesh, center_of_mass)
    normal, center = get_plane_information(occlusal_plane)


    # Step 4: Grid splitting and inclusion threshold calculation
    grid_cells, highest_points_segments, points_in_cells, inclusion_thresholds, point_and_grid_cell  = determine_high_point_and_grid_cells(mesh, cell_size, inclusion_criterion, bounds, normal, points)

    # Step 5: Soft tissue removal (cutting)
    distance_threshold = (max(inverted_mesh.vertices[:, 2]) - min(
        inverted_mesh.vertices[:, 2])) * distance_threshold_ratio

    cleaned_mesh = cutting_algorithm(mesh, grid_cells, point_and_grid_cell, inclusion_thresholds, points_in_cells, points, distance_threshold_ratio)

    # Step 6: Generate cleaned file path
    file_dir = os.path.expanduser("~/Dental_data_cleaned")
    os.makedirs(file_dir, exist_ok=True)
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))  # File name and extension
    cleaned_file_path = os.path.join(file_dir, f"{file_name}_cleaned{file_ext}")  # New file path with _cleaned

    # Save cleaned mesh to an STL file
    cleaned_mesh.write(cleaned_file_path)
    print(f"Cleaned mesh saved to: {cleaned_file_path}")

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time  # Compute elapsed time

    # Visualize the cleaned mesh
    #vedo.show([cleaned_mesh])

    # Return
    return cleaned_mesh #, elapsed_time










