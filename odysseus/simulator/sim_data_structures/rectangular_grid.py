import numpy as np
import pandas as pd
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd

from odysseus.simulator.sim_data_structures.squared_zone import SquaredZone


class RectangularGrid:

    def __init__(self, height, width):

        self.height = height
        self.width = width
        self.grid_matrix = []
        self.grid_dict = {}

        self.init_zoning()

    def init_zoning(self):

        x_min, y_min, x_max, y_max = (0, 0, self.width, self.height)
        x_left = 0
        x_right = self.width
        row = 0

        for i in range(self.width):
            y_top = y_max
            y_bottom = y_max - self.height
            self.grid_matrix.append([])
            col = 0
            for j in range(self.height):
                shape = Polygon([(x_left, y_top), (x_right, y_top), (x_right, y_bottom), (x_left, y_bottom)])
                zone_id = col * self.height + row
                zone = SquaredZone(zone_id=zone_id, shape=shape, x_grid=i, y_grid=j)
                self.grid_matrix[i].append(zone)
                self.grid_dict[zone_id] = zone
                y_top = y_top - self.height
                y_bottom = y_bottom - self.height
                col += 1
            row += 1
            x_left = x_left + self.width
            x_right = x_right + self.width

    def get_zone_from_id(self, zone_id):
        return self.grid_dict[zone_id]

    def get_zone_from_indices(self, i, j):
        return self.grid_matrix[i][j]

    def init_for_simulation(self, env, zones_vehicles_dict):
        for zone in self.grid_dict:
            self.grid_dict[zone].init_for_simulation(env, zones_vehicles_dict[zone])
