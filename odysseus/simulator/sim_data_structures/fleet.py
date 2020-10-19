import simpy
import random
import datetime

from odysseus.simulator.sim_data_structures.vehicle import Vehicle


class Fleet(object):

    def __init__(
            self,
            n_vehicles,
    ):
        self.n_vehicles = n_vehicles
        self.vehicles_dict = dict()
        for plate in range(self.n_vehicles):
            self.vehicles_dict[plate] = Vehicle(plate)

    def get_vehicle_from_plate(self, plate):
        return self.vehicles_dict[plate]

    def init_for_simulation(self, env, vehicles_zones_dict):
        for plate in range(self.n_vehicles):
            self.vehicles_dict[plate].init_for_simulation(env, vehicles_zones_dict[plate])
