# The visualizer class is used to show 3d point clouds or bounding boxes in the browser.

from .points import Points
from .cuboid import Cuboid
from .lines import Lines
import os
import sys
import shutil
import json
import numpy as np


class Visualizer:

    def __init__(self):
        self.elements = {}  # dict of elements to display

    def add_points(self, name, positions, colors=None, normals=None, point_size=25, visible=True):
        """Add points to the visualizer.

        :param name: The name of the points displayed in the visualizer.
        :param positions: The point positions.
        :param normals: The point normals.
        :param colors: The point colors.
        :param point_size: The point size.
        :param visible: Bool if points are visible.
        """
        if colors is None:
            colors = np.zeros(positions.shape)
        if normals is None:
            normals = np.ones(positions.shape)
        self.elements[name] = Points(positions, colors, normals, point_size, visible)

    def add_lines(self, name, lines_start, lines_end, colors=None, visible=True):
        """Add lines to the visualizer.

        :param name: The name of the lines displayed in the visualizer.
        :param lines_start: The start positions of the lines.
        :param lines_end: The end positions of the lines.
        :param colors: The line colors.
        :param visible: Bool if lines are visible.
        """
        self.elements[name] = Lines(lines_start, lines_end, colors, visible)

    def add_bounding_box(self, name, position, size, orientation=None):
        """Add bounding box.

        :param name: The bounding box name. (string)
        :param position: The center position. (float32, 3x1)
        :param size: The size. (float32, 3x1)
        :param orientation: The orientation (float32, 3x1)
        """
        self.elements[name] = Cuboid(position, size, orientation)

    def save(self, path, port=6008):
        """Creates the visualization and displays the link to it.

        :param path: The path to save the visualization files.
        :param port: The port to show the visualization.
        """

        # Delete destination directory if it exists already
        directory_destination = os.path.abspath(path)
        if os.path.isdir(directory_destination):
            shutil.rmtree(directory_destination)

        # Copy website directory
        directory_source = os.path.realpath(os.path.join(os.path.dirname(__file__), 'src'))
        shutil.copytree(directory_source, directory_destination)

        # Assemble binary data files
        nodes_dict = {}
        for name, e in self.elements.items():
            binary_file_path = os.path.join(directory_destination, name+'.bin')
            nodes_dict[name] = e.get_properties(name+'.bin')
            e.write_binary(binary_file_path)

        # Write json file containing all scene elements
        json_file = os.path.join(directory_destination, 'nodes.json')
        with open(json_file, 'w') as outfile:
            json.dump(nodes_dict, outfile)

        # Display link
        http_server_string = 'python -m SimpleHTTPServer ' + str(port)
        if sys.version[0] == '3':
            http_server_string = 'python -m http.server ' + str(port)
        print('')
        print('************************************************************************')
        print('1) Start local server:')
        print('    cd '+directory_destination+'; ' + http_server_string)
        print('2) Open in browser:')
        print('    http://localhost:' + str(port))
        print('************************************************************************')