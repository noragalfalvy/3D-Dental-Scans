# Cutting Algorithm
import numpy as np
import vedo

# Remove grids based on the distance threshold
def remove_grids_below_distance_threshold(mesh, grid_cells, point_and_grid_cell, distance_threshold, points):
    '''
    Function to remove points within grid cells whose highest points are below the distance threshold.

    Input: mesh, grid_cells, point_and_grid_cell, distance_threshold, points
    Output: modified_mesh, points_to_remove
    '''
    z_threshold = np.max(points[:, 2]) - distance_threshold
    # Identify grid cells to remove based on the threshold
    grids_to_remove = [i for i, p in point_and_grid_cell.items() if p[2] < z_threshold]

    # Filter out points in those grid cells
    points_to_remove = [
        idx for i in grids_to_remove for idx, v in enumerate(points)
        if grid_cells[i][0] < v[0] < grid_cells[i][1] and grid_cells[i][2] < v[1] < grid_cells[i][3]
    ]

    # Clone the mesh and remove points in specified cells
    modified_mesh = mesh.clone()
    modified_mesh.delete_cells_by_point_index(points_to_remove)
    return modified_mesh, points_to_remove

# Remove points below the inclusion threshold
def remove_points_below_inclusion_threshold(mesh, grid_cells, inclusion_thresholds, points_in_cells, points):
    '''
    Function to remove points from a mesh falling below specified inclusion thresholds in the z-coordinate.

    Input: mesh, grid_cells, inclusion_thresholds, points_in_cells, points
    Output: cleaned mesh
    '''
    indices_to_keep = set()

    # Iterate over each cell and check points against the inclusion threshold
    for cell_index, inclusion_threshold in enumerate(inclusion_thresholds):
        points_in_cell = points_in_cells[cell_index]

        # Keep points above or at the z threshold
        valid_points = points_in_cell[points_in_cell[:, 2] >= inclusion_threshold[2]]
        global_indices = np.where(np.isin(points, valid_points).all(axis=1))[0]
        indices_to_keep.update(global_indices)

    # Clone and filter the mesh
    cleaned_mesh = mesh.clone()
    points_to_remove = set(range(len(points))) - indices_to_keep
    cleaned_mesh.delete_cells_by_point_index(list(points_to_remove))

    return cleaned_mesh

# Cutting Algorithm
def cutting_algorithm(mesh, grid_cells, point_and_grid_cell, inclusion_thresholds, points_in_cells, points, distance_threshold_ratio):
    '''
    Function to perform both cuts

    Input: mesh, grid_cells, inclusion_thresholds, points_in_cells, points, distance_threshold_ratio
    Output: cleaned mesh
    '''
    # 1. Calculate distance threshold
    z_range = max(points[:, 2]) - min(points[:, 2])
    distance_threshold = z_range * distance_threshold_ratio

    # 2. First cut
    modified_mesh, points_to_remove = remove_grids_below_distance_threshold(mesh, grid_cells, point_and_grid_cell, distance_threshold, points)

    # 3. Second cut. Remove indices below inclusion threshold
    cleaned_mesh = remove_points_below_inclusion_threshold(mesh, grid_cells, inclusion_thresholds, points_in_cells, points)

    # 4. Return cleaned mesh
    return cleaned_mesh

