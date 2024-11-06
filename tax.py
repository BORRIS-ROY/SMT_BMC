import random
import heapq
import math
import collections

class Taxi:
    def __init__(self, taxi_id, color, x, y):
        self.id = taxi_id
        self.color = color
        self.x = float(x)
        self.y = float(y)
        self.current_fare = None
        self.total_earnings = 0
        self.total_fares = 0
        self.path = []
        self.movements = 0

    @property
    def has_fare(self):
        return self.current_fare is not None

    # The move method, taxis move twords junctions
    def move(self, junctions, streets):
        if self.current_fare:
            if not self.path:
                start_junction = self.find_current_junction(junctions)
                destination_junction = self.current_fare.destination
                self.path = self.a_star(start_junction, destination_junction, junctions, streets)
    
            if self.path:
                next_junction = self.path[0]
                if self.is_at_junction(next_junction):
                    # Move to the next junction in the path
                    self.path.pop(0)  
    
                    if self.is_at_junction(self.current_fare.destination):
                        self.drop_off_fare()
                else:
                    self.move_towards(next_junction)


    #def is_at_junction(self, junction):
    def is_at_position(self, position):
        return round(self.x) == position[0] and round(self.y) == position[1]
    def is_at_junction(self, junction):
        """
        Check if the taxi is currently at the specified junction.
        """
        return round(self.x) == junction.x and round(self.y) == junction.y

    def move_towards(self, next_junction):
        dx = next_junction.x - self.x
        dy = next_junction.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
    
        # Move a small step towards the next junction
        if distance > 0:
            step_x = dx / distance
            step_y = dy / distance
    
            self.x += step_x
            self.y += step_y

    def find_current_junction(self, junctions):
        """
        Find the nearest junction to the taxi's current position.
        """
        for junction in junctions:
            if self.is_at_junction(junction):
                return junction
        return None

    def pick_up_fare(self, fare, fares):
        self.current_fare = fare
        self.total_fares += 1
        fares.remove(fare)
        self.path = []  
        #print(f"Taxi {self.id} picked up fare to ({fare.destination.x}, {fare.destination.y})")

    def drop_off_fare(self):
        if self.current_fare:
            if self.is_at_junction(self.current_fare.destination):
                self.total_earnings += self.calculate_fare_price()
                #print(f"Taxi {self.id} dropped off fare at ({self.current_fare.destination.x}, {self.current_fare.destination.y}). Total earnings: £{self.total_earnings}")
                self.current_fare.mark_as_dropped_off()
                self.current_fare = None
                self.path = []
                self.movements = 0

    def a_star(self, start, goal, junctions, streets):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {junction: float('inf') for junction in junctions}
        g_score[start] = 0
        f_score = {junction: float('inf') for junction in junctions}
        f_score[start] = self.heuristic(start, goal)
    
        while open_set:
            _, current = heapq.heappop(open_set)
    
            if current == goal:
                return self.reconstruct_path(came_from, current)
    
            for neighbor in self.get_adjacent_junctions(current, junctions, streets):
                tentative_g_score = g_score[current] + self.distance_to(current, neighbor)
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
        return []
    
    

    def get_adjacent_positions(self, current_position, streets):
        """
        Get adjacent positions along the streets, including intermediate points between junctions.
        """
        adjacent_positions = []
        
        for street in streets:
            start_x, start_y = street.nodeA
            end_x, end_y = street.nodeB
            
            # Check if the current position is on this street
            if self.is_on_street(current_position, street):
                # Add intermediate positions along the street
                num_steps = max(abs(end_x - start_x), abs(end_y - start_y))
                step_x = (end_x - start_x) / num_steps
                step_y = (end_y - start_y) / num_steps
                
                for i in range(1, num_steps):
                    new_x = start_x + i * step_x
                    new_y = start_y + i * step_y
                    adjacent_positions.append((new_x, new_y))
                
                # Add the street endpoints as valid positions
                adjacent_positions.append((start_x, start_y))
                adjacent_positions.append((end_x, end_y))
        
        return adjacent_positions
    
    def is_on_street(self, current_position, street):
        """
        Check if the current position is on the given street.
        """
        start_x, start_y = street.nodeA
        end_x, end_y = street.nodeB
        
        # Check if the position lies on the line segment between nodeA and nodeB
        if min(start_x, end_x) <= current_position[0] <= max(start_x, end_x) and \
           min(start_y, end_y) <= current_position[1] <= max(start_y, end_y):
            return True
        return False

    def reconstruct_path(self, came_from, current):
        """
        Reconstruct the path from start to goal.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def heuristic(self, junction, goal):
        """
        Heuristic function for A* (Manhattan distance).
        """
        return abs(junction.x - goal.x) + abs(junction.y - goal.y)

    def distance_to(self, junction, neighbor):
        """
        Calculate the Manhattan distance between two junctions.
        """
        return abs(junction.x - neighbor.x) + abs(junction.y - neighbor.y)

    def calculate_fare_price(self):
        """
        Calculate the fare price based on distance or any other logic.
        """
        
        return 10  # Example fixed fare price
    
    # BFS ALgorithm
    def bfs(self, start, goal, junctions, streets):
        queue = collections.deque([start])  
        came_from = {start: None}  
    
        while queue:
            current = queue.popleft()  
    
            if current == goal:
                return self.reconstruct_path(came_from, current)   
    
            for neighbor in self.get_adjacent_junctions(current, junctions, streets):
                if neighbor not in came_from:  
                    queue.append(neighbor)  
                    came_from[neighbor] = current 
    
        return []  # Return empty if no path found
    
    # DFS
    def dfs(self, start, goal, junctions, streets):
        stack = [start]  
        came_from = {start: None}  
    
        while stack:
            current = stack.pop()  
    
            if current == goal:
                return self.reconstruct_path(came_from, current)   
    
            for neighbor in self.get_adjacent_junctions(current, junctions, streets):
                if neighbor not in came_from:  
                    stack.append(neighbor)  
                    came_from[neighbor] = current 
    
        return []  # Return empty if no path found


