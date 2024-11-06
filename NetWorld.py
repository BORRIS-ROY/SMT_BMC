import random
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
import time
class Fare:
    def __init__(self, origin, destination):
        """
        Initialize a Fare with an origin and destination, which are tuples representing (x, y) coordinates.
        """
        self.origin = origin
        self.destination = destination
        self.x = origin.x
        self.y = origin.y
        self.is_picked_up = False
        self.color = YELLOW  # Default color for fares
        self.pickup_time = None
        self.dropoff_time = None
        self.is_dropped_off = False 

    def assign_taxi(self, taxi):
        """
        Assign the taxi to pick up the fare.
        """
        self.is_picked_up = True
        taxi.current_fare = self
    def mark_as_dropped_off(self):
        self.dropoff_time = time.time() # Record the drop-off time
        self.is_dropped_off = True 
        self.color = RED

    def get_completion_time(self):
        if self.pickup_time and self.dropoff_time:
            return self.dropoff_time - self.pickup_time
        return None


class NetWorld:
    def __init__(self, junctions, streets):
        """
        Initialize the world with a set of junctions and streets.
        """
        self.junctions = junctions
        self.streets = streets
        self.fares = []
        self.taxis = []

    def place_fares(self, num_fares):
        """
        Randomly place fares at junctions in the world.
        """
        for _ in range(num_fares):
            src_junction = random.choice(self.junctions)
            dest_junction = random.choice(self.junctions)
            while src_junction == dest_junction:
                dest_junction = random.choice(self.junctions)
            fare = Fare(src_junction, dest_junction)
            self.fares.append(fare)
        return self.fares

    def add_taxi(self, taxi):
        """
        Add a taxi to the world.
        """
        self.taxis.append(taxi)

    def get_adjacent_junctions(self, current_junction):
        """
        Given a junction, find the adjacent junctions connected by streets.
        """
        adjacent = []
        for street in self.streets:
            if current_junction == self.junctions[street.start_point]:
                adjacent.append(self.junctions[street.end_point])
            elif current_junction == self.junctions[street.nodeB]:
                adjacent.append(self.junctions[street.nodeA])
        return adjacent
    
    