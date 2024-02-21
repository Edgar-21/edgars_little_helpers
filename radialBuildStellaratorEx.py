from plotRadialBuildStellarator import plotRadialBuild

import numpy as np

phi_list = [0.0, 22.5, 45.0, 67.5, 90.0]
# Define poloidal angles at which radial builds is specified.
# Note that this should always span 360 degrees.
theta_list = [0.0, 90.0, 180.0, 270.0, 360.0]

# Define radial build
# For each component, thickness matrices have rows corresponding to toroidal
# angles (phi_list) and columns corresponding to poloidal angles (theta_list)
build = {
    'phi_list': phi_list,
    'theta_list': theta_list,
    'wall_s': 1.2,
    'radial_build': {
        'first_wall': {
            'thickness_matrix': np.ones((len(phi_list), len(theta_list)))*5
        },
        'breeder': {
            'thickness_matrix': [
                [80, 40, 20, 40, 80],
                [50, 40, 30, 30, 50],
                [30, 30, 25, 30, 30],
                [50, 30, 30, 40, 50],
                [80, 40, 20, 40, 80]
            ]
        },
        'back_wall': {
            'thickness_matrix': np.ones((len(phi_list), len(theta_list)))*5
        },
        'shield': {
            'thickness_matrix': [
                [50, 25, 15, 25, 50],
                [30, 25, 20, 20, 30],
                [20, 20, 15, 20, 20],
                [30, 20, 20, 25, 30],
                [50, 25, 15, 25, 50]
            ]
        },
        # Note that some neutron transport codes (such as OpenMC) will interpret
        # materials with "vacuum" in the name as void material
        'vacuum_vessel': {
            'thickness_matrix': np.ones((len(phi_list), len(theta_list)))*15,
            'h5m_tag': 'vac_vessel'
        }
    }
}

plotRadialBuild(build, 1, 3, 'Example Radial Build')
