import read_vmec
import numpy as np
from scipy.optimize import newton


def magnitude(vec_list):
    """return the magnitudes of a list of vectors

    Arguments:
        vec_list (NX3 np array)

    Returns:
        magnitude_list (NX1 np_array)
    """
    magnitude_list = vec_list[:, 0]**2 + vec_list[:, 1]**2 + vec_list[:, 2]**2
    magnitude_list = np.sqrt(magnitude_list)

    return magnitude_list


def dot(vec1, vec2):
    """ Returns a list of the dot products of 2 lists of vectors

    Arguments:
        vec1 (NX3 np array)
        vec2 (NX3 np array)

    returns:
        dot_list (NX1 np array)
    """
    dot_list = vec1[:, 0]*vec2[:, 0]+vec1[:, 1] * \
        vec2[:, 1]+vec1[:, 2]*vec2[:, 2]

    return dot_list


def cross(vec1, vec2):
    """ Returns a list of the cross products of 2 lists of vectors

    Arguments:
        vec1 (NX3 np array)
        vec2 (NX3 np array)

    returns:
        cross_list (NX3 np array)
    """

    i_list = vec1[:, 1]*vec2[:, 2]-vec1[:, 2]*vec2[:, 1]
    j_list = vec1[:, 2]*vec2[:, 0]-vec1[:, 0]*vec2[:, 2]
    k_list = vec1[:, 0]*vec2[:, 1]-vec1[:, 1]*vec2[:, 0]

    cross_list = np.array([i_list, j_list, k_list]).T

    return cross_list


def get_theta_guesses(num_theta_guesses, phi_coords, coords, wall_s, vmec):
    """
    Calculate the distances between the plasma surface and the coordinate at 
    each theta, phi combination and keep the theta that gets the smallest 
    distance as an initial guess

    this might be better as a minimization routine
    """
    theta_grid = np.linspace(0, 2*np.pi, num_theta_guesses)

    theta_guesses = []
    distances = []
    for phi, coord in zip(phi_coords, coords):
        least_distance = None
        kept_theta = None
        for theta in theta_grid:
            plasma_point = np.array(vmec.vmec2xyz(wall_s, theta, phi))*100
            distance = np.sqrt(np.sum(np.square(coord-plasma_point)))
            if least_distance is not None:
                if distance < least_distance:
                    least_distance = distance
                    kept_theta = theta
            else:
                kept_theta = theta
                least_distance = distance
        theta_guesses.append(kept_theta)
        distances.append(least_distance)

    return np.array(theta_guesses)


def residual(theta_guesses, phi_coords, coords, wall_s, vmec, boink=1e-6):
    """
    compute normal at theta_guesses, calculate how close each normal comes to
    each centroid, return that value for each theta guess as the residual

    each phi has a corresponding plane. The tangent vector and normal vector
    will lie in this plane

    this might actually be much faster as an element wise function as some
    elements take much longer to converge than others ~100x in some cases

    Arguments:
        theta_guess (1D numpy array): guessed theta coordinates in radians
        phi_coords (1D numpy array): phi coordinate corresponding to theta 
        guesses coords (numpy array of XYZ): centroid of mesh element for
            which to findtheta, phi
        wall_s (float): wall_s vmec parameter for the surface to offset from
        vmec (read_vmec object): plasma equilibrium information
        boink (float): amount to peturb theta by for calculating tangent

    returns:
        distances (1D numpy array): perpendicular distance each calculated 
            poloidal vector is from the corresponding centroid. If the centroid
            is found to be below the plane formed by the tangent and toroidal
            normal then this value is artifically increased substantially to 
            encourage the correct one of the two roots to be found.
    """
    point_set1 = []
    point_set2 = []

    for theta_guess, phi_coord in zip(theta_guesses, phi_coords):

        theta_guess_boinked = theta_guess+boink

        # check for numerical difficulties
        if theta_guess == theta_guess_boinked:
            print('bad value for theta at phi, theta', phi_coord, theta_guess)

        point_set1.append(np.array(vmec.vmec2xyz(
            wall_s, theta_guess, phi_coord))*100)
        point_set2.append(np.array(vmec.vmec2xyz(
            wall_s, theta_guess_boinked, phi_coord))*100)

    point_set1 = np.array(point_set1)
    point_set2 = np.array(point_set2)

    offset_vectors = coords-point_set1

    phi_plane_normals = np.array(
        [-np.sin(phi_coords),
         np.cos(phi_coords),
         np.zeros(len(phi_coords))]).T

    tangents = point_set2 - point_set1

    normals = cross(phi_plane_normals, tangents)

    distances = magnitude(cross(offset_vectors, normals))/magnitude(normals)

    # need to also check if the point is on the right side of the plane
    # formed by tangent and phi_normal
    a = normals[:, 0]
    b = normals[:, 1]
    c = normals[:, 2]
    d = a*point_set1[:, 0]+b*point_set1[:, 1]+c*point_set1[:, 2]

    # so calculate first if the point is above or below the plane

    orientations = a*coords[:, 0]+b*coords[:, 1]+c*coords[:, 2]-d

    # then find the distance

    distances_to_plane = np.abs(a*coords[:, 0]+
                                b*coords[:, 1]+
                                c*coords[:, 2]+d)/(
                                np.sqrt(np.square(a)+ 
                                        np.square(b)+ 
                                        np.square(c)))

    # then if its negative add the absolute value to distances
    # if its not then add 0 to distances

    distances_to_plane = np.where(
        orientations < 0, distances_to_plane, np.zeros(len(orientations)))
    distances += distances_to_plane

    return distances


def unwind_thetas(thetas):
    new_thetas = thetas % (2*np.pi)
    new_thetas = np.where(thetas < 0, new_thetas, new_thetas)
    return new_thetas


def centroids_to_theta_phi(centroids, wall_s, vmec, num_theta_guesses,
                           max_iter):
    """
    get the phi, theta coordinate pairs that, when offseting in the poloidal
    normal from the surface described by wall_s, results in the normal
    passing through the centroid.

    if this is failing to converge, hopefully just increasing max_iter will
    help. I have used 5000 in the past. The speed may also be enhanced by
    switching this to elementwise operations, since different elements take
    different numbers of iterations to converge, sometimes hundreds more 
    iterations.

    Arguments:
        centroids (np array of x,y,z): points at which to perform the above 
            root finding
        wall_s (float): vmec parameter for the surface of interest
        vmec (read_vmec object): representation of plasma equilibrium
        num_theta_guesses (int): number of evenly spaced theta points to check
            to determine the starting point for rootfinding
        max_iter (int): maximum iterations before declaring that the root
            has failed to converge.

    """
    # calculate phi angles for each centroid
    phi_coords = np.arctan2(centroids[:, 1], centroids[:, 0])

    theta_guesses = get_theta_guesses(
        num_theta_guesses, phi_coords, centroids, wall_s, vmec)

    theta_coords = newton(residual, theta_guesses, args=(
        phi_coords, centroids, wall_s, vmec), maxiter=max_iter)

    theta_coords = unwind_thetas(theta_coords)

    return phi_coords, theta_coords
