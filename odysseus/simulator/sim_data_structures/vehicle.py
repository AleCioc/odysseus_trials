import simpy
import random
import datetime


class Vehicle(object):

    def __init__(
            self,
            plate,
    ):

        self.plate = plate

        self.env = None
        self.zone = None
        self.available = False
        self.soc = 0
        self.current_status = {}
        self.status_dict_list = []

    def update_status(self, time, available, status, soc, zone):
        self.current_status = {
            "time": time,
            "available": available,
            "status": status,
            "soc": soc,
            "zone": zone.zone_id
        }
        print(self.current_status)
        self.status_dict_list.append(self.current_status)

    def init_for_simulation(self, env, zone):

        self.env = env
        self.zone = zone
        self.soc = simpy.Container(env, init=100, capacity=100)
        self.update_status(0, True, 'parked', self.soc.level, zone)

    def booking(self, booking_request):

        self.update_status(
            booking_request["start_time"], True, 'booked', self.soc.level, booking_request['origin']
        )
        booking_request['origin'].remove_vehicle(self, booking_request["start_time"])

        yield self.env.timeout(booking_request["end_time"] - booking_request["start_time"])
        self.soc.get(1)

        self.update_status(
            booking_request["end_time"], True, 'booked', self.soc.level, booking_request['destination']
        )
        booking_request['destination'].add_vehicle(self, booking_request["end_time"])
