import os
import unittest
import simpy

from odysseus.simulator.sim_data_structures.fleet import Fleet
from odysseus.simulator.sim_data_structures.rectangular_grid import RectangularGrid


def create_booking_request(
        start_time,
        end_time,
        origin,
        destination,
):

    booking_request = dict()
    booking_request["start_time"] = start_time
    booking_request["end_time"] = end_time
    booking_request["origin"] = origin
    booking_request["destination"] = destination
    return booking_request


def generate_single_request(env, rectangular_grid):
    for i in range(1):
        origin = rectangular_grid.get_zone_from_id(0)
        destination = rectangular_grid.get_zone_from_id(2)
        booking_request = create_booking_request(
            3, 10, origin, destination
        )
        vehicle = origin.search_vehicle()
        if vehicle is not None:
            yield env.process(vehicle.booking(booking_request))


class TestVehicleMovements(unittest.TestCase):

    def setUp(self):
        pass

    def test_single_vehicle(self):

        # Create city zones
        rectangular_grid = RectangularGrid(2, 2)

        # Create fleet
        fleet = Fleet(1)

        # Create SimPy environment
        env = simpy.Environment()

        # Assign vehicles to zones
        vehicles_zones_dict = {
            0: rectangular_grid.get_zone_from_id(0)
        }
        zones_vehicles_dict = {
            0: [fleet.get_vehicle_from_plate(0)],
            1: [],
            2: [],
            3: [],
        }

        # Initialise fleet for simulation
        fleet.init_for_simulation(env, vehicles_zones_dict)

        # Initialise grid for simulation
        rectangular_grid.init_for_simulation(env, zones_vehicles_dict)

        env.process(generate_single_request(env, rectangular_grid))
        env.run(until=20)

    def tearDown(self):
        pass
