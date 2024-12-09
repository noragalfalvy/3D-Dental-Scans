# Occlusal Plane Approximation Algorithm
# Import Required Packages
import vedo
import numpy as np

# Function to perform initiall PCA Analysis
def calculate_pca_axes(mesh, center_of_mass):
    '''
    Function to determine the distribution of tthe variance of the data through a PCA

    Input: Inverted dental mesh
    Output: Eigenvectors later to be used to create the planes

    Goal:
    To determine the centroid of the mesh, and get the principal components from the centroid
    The principal components reprents the directions of maximun variance.
    '''
    # 1. Reduce the number of points by using the vedo function "cut_with_plane"
    cutted_mesh = mesh.clone().cut_with_plane(origin=center_of_mass, normal='z')

    # 2. Get all the vertices
    cutted_mesh_points = cutted_mesh.vertices
    # 2.1 Only use X and Y
    points_xy = cutted_mesh_points[:, :2]
    # 2.2. Center all points according to the centroid of the mesh
    '''
    points_xy refers to the points in the x and y axis
    np.mean(points_xy) refers to the mean of the x and y coordinates
    when we substract these two, we are centering the points
    this is necessary in PCA in order to get the directions with the maximun variance from the center
    '''
    centered_points = points_xy - np.mean(points_xy, axis=0)

    # 3. Perform a PCA
    cov_matrix = np.cov(centered_points, rowvar=False) # Covariance matrix. rowvar=False implies we are transposing: the columns are variables (X and Y) and the rows are obs (Points)
    eig_vectors = np.linalg.eigh(cov_matrix)[1] # eig vectors. So here we get the principal directions of the variation of the data. We use [1] bc the [0] refers to the eig_values

    # 4. Return vectors
    return eig_vectors[:, ::-1]  # Descending order so the first vector has the greates variance

# Cut function using the planes
def cut_mesh(mesh, center_of_mass):
    '''
    Function to cut the mesh using the planes that have the normals as the eigenvectors previously calculated

    Input: Inverted dental mesh, center of mass of the mesh
    Output: Segmented mesh and cutting planes.
    '''
    # 1. Calculate pca axes
    pca_axes_xy = calculate_pca_axes(mesh, center_of_mass) #here we get the eigen vectors

    # 2. Add a null Z component to work in 3D
    pca_axes = np.zeros((3, 3)) # temporary matrix of 0 to use the Z line from. This is only to keep the structure
    pca_axes[:2, :2] = pca_axes_xy  # Insert XY vectors into the 3D matrix (keeping Z=0)

    # pca_axes is the matrix containing the two principal components (First and second column) while the third is full of zeroes (Z axis)

    # 3. Create the planes
    planes = []
    n_planes = min(2, pca_axes.shape[1])  # Determine the number of planes
    for i in range(n_planes):
        # Use XY axis as normals
        normal = pca_axes[:, i]  # we iterate over all the columns of the matrix (we iterate over each principal component)
        # Here we create planes that go through the center of mass but use the principal components as the normals
        plane = vedo.shapes.Plane(pos=center_of_mass, normal=normal, s=(100, 100))
        planes.append(plane)

    # 4. Cut the mesh into segments using the planes
    cutted_mesh = mesh.clone().cut_with_plane(origin=center_of_mass, normal='z')
    segments = [cutted_mesh]
    for plane in planes:
        new_segments = []
        for segment in segments:
            # 4.1 Cut each segment using the each plane per iteration
            cut1 = segment.clone().cut_with_plane(origin=plane.pos(), normal=plane.normal)
            cut2 = segment.clone().cut_with_plane(origin=plane.pos(), normal=-(plane.normal))

            # 4.2 Only add non empty segments
            if cut1.npoints > 0:
                new_segments.append(cut1)
            if cut2.npoints > 0:
                new_segments.append(cut2)

        segments = new_segments

    # 5. Retun segments of the dental mesh and the planes
    return segments, planes

# Function to get the highest points
def highest_points(segments):
    '''
    Function to determine the highest points of each segment of the mesh

    Input: segments of the mesh.
    Output: numpy array of the coordinates of the highest points
    '''
    # 1. Create list
    highest_points = []

    # 2. Iterate over each segment
    for i, segment in enumerate(segments): #enumerate is useful to get both the element and the index of the list
        # 2.1 Use the vertices from the segments
        segment_points = segment.vertices

        # Highest z point
        if segment_points.size >0:
            highest_z = max(segment_points, key=lambda p: p[2])  # p[2] refers to z # lambda is an annonymus function. Here we are telling lambda to take the point "p" and only look at the z coordinate.
            highest_points.append(highest_z)

    return np.array(highest_points)

# Occlusal plane function
def occlusal_plane_algorithm(mesh, center_of_mass):
    '''
    Function to generate the occlusal plane of the dental mesh.

    Input: The inverted mesh.
    Output: Approximation of the occlusal plane in the form of a vedo object.
    '''
    #Use previously defined functions
    segments, planes = cut_mesh(mesh, center_of_mass)
    high_points_segments = highest_points(segments)

    # Convert it to vedo
    vedo_points = vedo.Points(high_points_segments, c='red', r=12)

    #Create plane
    #print(vedo_points)
    new_plane = vedo.fit_plane(vedo_points).c('blue')
    return new_plane

# Get the information from the plane
def get_plane_information(plane):
    '''
    Function to get the information about the occlusal plane

    Input: The occlusal plane.
    Output: Information about the occlusal plane (normal and center of mass).
    '''
    normal = plane.normal
    center = plane.center
    return normal, center






