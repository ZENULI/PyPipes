"""
# This files originate from the "PyPipes" project:
#   https://github.com/ZENULI/PyPipes
# Created by ZENULI at University Paul Sabatier III :
#   https://github.com/BastienKovac
#   https://github.com/Ulynor
#   https://github.com/seb2s
# License:
#   MIT License Copyright (c) 2022 ZENULI
"""


import random
import numpy as np
import random
import pathlib
import open3d as o3d


def get_part_mesh(part_type):
    resource_dir = pathlib.Path(__file__).parent.parent / "resources" / "3Dmodels"

    return {
        'COUDE': o3d.io.read_triangle_mesh(str(resource_dir / "coude.ply")),
        'TE': o3d.io.read_triangle_mesh(str(resource_dir / "te.ply")),
        'PIPE1': o3d.io.read_triangle_mesh(str(resource_dir / "pipe1.ply")),
        'PIPE2': o3d.io.read_triangle_mesh(str(resource_dir / "pipe2.ply")),
        'PIPE3': o3d.io.read_triangle_mesh(str(resource_dir / "pipe3.ply")),
        'PIPE4': o3d.io.read_triangle_mesh(str(resource_dir / "pipe4.ply")),
        'CROSS': o3d.io.read_triangle_mesh(str(resource_dir / "cross.ply"))
    }.get(part_type, 0)


def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    """Finds angle between two vectors"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def vector_x_rotation(vector, theta):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    return np.dot(R, vector)


def vector_y_rotation(vector, theta):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R, vector)


def vector_z_rotation(vector, theta):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return np.dot(R, vector)


def get_z_rotation_matrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])


def random_rotation_vector():
    rx = random.randrange(0, 90, 15)
    ry = random.randrange(0, 90, 15)
    rz = random.randrange(0, 90, 15)
    return np.asarray([rx, ry, rz])


def random_coordinate():
    x = random.randrange(0, 90, 15)  # changer
    y = random.randrange(0, 90, 15)
    z = random.randrange(0, 90, 15)
    return np.asarray([x, y, z])


def random_right_direction(father_direction, part_type):
    new_direction = father_direction
    if ((part_type != 'PIPE1') and (part_type != 'PIPE2') and (part_type != 'PIPE2') and (
            part_type != 'PIPE4')):  # changer
        new_direction = vector_y_rotation(father_direction, random.randrange(2) * np.pi)
    return new_direction


def get_mesh_size(part_type, part_right_direction):  # size of a mesh from the center and in a given direction

    aligned = np.dot(unit_vector(part_right_direction), np.asarray([0., 0., 1.]))

    if (aligned == 1):
        return {
            'COUDE': 0.910665,
            'TE': 1.284005,
            'CROSS': 1.284005,
            'PIPE1': 1.784005,
            'PIPE2': 2.97334,
            'PIPE3': 5.6493,
            'PIPE4': 2.97334
        }.get(part_type, 0)
    elif (aligned == 0):
        return {
            'COUDE': 0.87039,
            'TE': 1.284005,
            'CROSS': 1.284005,
        }.get(part_type, 0)
    else:
        # erreur
        return 1


def compute_part_coordinate(father_type, father_coordinate, father_right_direction, father_radius, part_type,
                            part_right_direction, part_radius):
    father_direction_size = get_mesh_size(father_type, father_right_direction)
    father_scale_factor = 1 / father_radius

    part_direction_size = get_mesh_size(part_type, part_right_direction)
    part_scale_factor = 1 / part_radius

    part_coordinate = father_coordinate
    part_coordinate[2] += father_direction_size * father_scale_factor + part_direction_size * part_scale_factor

    return part_coordinate


def get_next_part(father_type, father_right_direction, father_coordinate,
                  father_radius):  # changer : en ft cest la lecture des noeuds du graphe

    part_type = random.choice(['TE', 'CROSS', 'PIPE1', 'PIPE2'])
    part_radius = 1
    # part_radius = random.uniform(min_radius, max_radius)
    # part_right_direction = random_right_direction(father_right_direction, part_type)
    part_right_direction = father_right_direction
    # part_z_rotation_vector = random_rotation_vector()
    part_z_rotation_vector = np.asarray([0., 0., 0.])
    # lors de la construction du graphe
    part_coordinate = compute_part_coordinate(father_type, father_coordinate, father_right_direction, father_radius,
                                              part_type, part_right_direction, part_radius)

    return part_radius, part_right_direction, part_type, part_z_rotation_vector, part_coordinate


def set_part_mesh(part_mesh, part_coordinate, part_right_direction, part_matrix_rotation, part_radius):
    # part_mesh = get_part_mesh(part_type)
    part_mesh.translate(part_coordinate, relative=True)  #
    part_mesh.rotate(part_matrix_rotation, center=(0, 0, 0))
    scale_factor = 1 / part_radius
    part_mesh.scale(scale_factor, center=part_mesh.get_center())

    return part_mesh


def pipelinecreator():
    resource_dir = pathlib.Path(__file__).parent.parent / "resources" / "3Dmodels"
    mesh = o3d.io.read_triangle_mesh(str(resource_dir / "empty.ply"))

    print(str(resource_dir / "empty.ply"))

    # lecture du graphe

    # direction à la racine  #lecture du graphe
    father_right_direction = np.asarray([0., 0., 1.])
    # father_coordinate = random_coordinate()
    father_coordinate = np.asarray([0., 0., 0.])
    father_radius = 1
    father_type = "CROSS"
    father_z_rotation_vector = np.asarray([0., 0., 0.])

    ####

    father_mesh = get_part_mesh(father_type)
    father_matrix_rotation = father_mesh.get_rotation_matrix_from_xyz(father_z_rotation_vector)
    part_matrix_rotation = get_z_rotation_matrix(random.randrange(0, 180, 5))

    father_mesh = set_part_mesh(father_mesh, father_coordinate, father_right_direction, father_matrix_rotation,
                                father_radius)
    mesh += father_mesh

    ####

    for i in range(nb_parts):  # lecture du graphe

        # itérer sur  chaque noeud

        part_radius, part_right_direction, part_type, part_z_rotation_vector, part_coordinate = get_next_part(
            father_type, father_right_direction, father_coordinate, father_radius)

        part_mesh = get_part_mesh(part_type)
        part_matrix_rotation = part_mesh.get_rotation_matrix_from_xyz(part_z_rotation_vector)
        part_matrix_rotation = get_z_rotation_matrix(random.randrange(0, 180, 5))

        part_mesh = set_part_mesh(part_mesh, part_coordinate, part_right_direction, part_matrix_rotation, part_radius)
        mesh += part_mesh

        ###

        father_coordinate = part_coordinate
        father_type = part_type
        father_right_direction = part_right_direction
        father_radius = part_radius

    mesh.compute_vertex_normals()

    return mesh


if __name__ == '__main__':
    nb_parts = 15
    min_radius = 1.0
    max_radius = 5.0

    mesh = pipelinecreator()

    box = mesh.get_axis_aligned_bounding_box()
    box.color = (1, 0, 0)

    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])

    o3d.visualization.draw_geometries([mesh, mesh_frame, box])