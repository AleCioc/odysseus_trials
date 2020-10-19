class SquaredZone(object):

    def __init__(self, zone_id, shape, x_grid, y_grid):

        self.zone_id = zone_id
        self.shape = shape
        self.x_grid = x_grid
        self.y_grid = y_grid

        self.env = None
        self.current_status = {}
        self.status_dict_list = []
        self.vehicles = []

    def update_status(self, time):
        self.current_status = {
            "t": time,
            "vehicles_parked": len(self.vehicles),
        }
        self.status_dict_list.append(self.current_status)

    def init_for_simulation(self, env, vehicles):
        self.env = env
        self.vehicles = vehicles
        self.update_status(0)

    def add_vehicle(self, vehicle, t):
        self.vehicles.append(vehicle)
        self.update_status(t)

    def remove_vehicle(self, vehicle, t):
        self.vehicles.remove(vehicle)
        self.update_status(t)

    def search_vehicle(self):
        for vehicle in self.vehicles:
            if vehicle.soc.level > 0:
                return vehicle
        return None
