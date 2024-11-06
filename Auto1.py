import pygame
import sys
import time
import random
from junc1 import junctions, streets
from tax import Taxi
from NetWorld import NetWorld, Fare
from z3 import Solver, Int, And, Or, Not, sat, If
from itertools import combinations
import time
import tracemalloc
networld = NetWorld(junctions, streets)

# Define constants
CELL_SIZE = 10
ROAD_WIDTH = 6
MOVE_INTERVAL = 30
FARE_INTERVAL = 300
NUM_FARES = 20
NUM_PARKED_CARS = 3

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Corn color
BLUE = (0, 0, 255)  # Parked car color
GREEN = (0, 255, 0)
DROPPED_OFF_COLOR = (30, 144, 255)  # DodgerBlue color for dropped-off fares

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Auto Taxi')

# Calculate grid size
grid_width = (max(junction.x for junction in junctions) + 1) * CELL_SIZE
grid_height = (max(junction.y for junction in junctions) + 1) * CELL_SIZE

# Set grid offset to move it to the left-hand side
OFFSET_X = 50
OFFSET_Y = (screen_height - grid_height) // 2

# Revenue meter settings
METER_WIDTH = 200
METER_HEIGHT = 20
METER_SPACING = 10
METER_START_X = screen_width - METER_WIDTH - 50
METER_START_Y = 50

dropped_texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
dropped_texture.fill(DROPPED_OFF_COLOR)

dropped_off_fares = []
# Function to draw the junctions
def draw_junctions():
    for junction in junctions:
        pygame.draw.circle(screen, GREY, (OFFSET_X + junction.x * CELL_SIZE, OFFSET_Y + junction.y * CELL_SIZE), 4)

# Function to draw the streets
def draw_streets():
    for street in streets:
        # Extract the start and end points from nodeA and nodeB
        start_pos = (OFFSET_X + street.nodeA[0] * CELL_SIZE, OFFSET_Y + street.nodeA[1] * CELL_SIZE)
        end_pos = (OFFSET_X + street.nodeB[0] * CELL_SIZE, OFFSET_Y + street.nodeB[1] * CELL_SIZE)
        pygame.draw.line(screen, GREY, start_pos, end_pos, ROAD_WIDTH)

# Function to draw the taxis
def draw_taxis(taxis):
    for taxi in taxis:
        pygame.draw.rect(screen, taxi.color, (OFFSET_X + taxi.x * CELL_SIZE - 4, OFFSET_Y + taxi.y * CELL_SIZE - 4, 8, 8))

# Function to draw the fares as corn-shaped
def draw_fares(fares, parked_cars):
    for fare in fares:
        fare_position = (fare.x, fare.y)
        
        # Check if the fare position is not occupied by a parked car
        if fare_position not in parked_cars:
            x = OFFSET_X + fare.x * CELL_SIZE
            y = OFFSET_Y + fare.y * CELL_SIZE
            points = [(x, y-4), (x+2, y-2), (x+4, y), (x+2, y+2), (x, y+4), (x-2, y+2), (x-4, y), (x-2, y-2)]
            pygame.draw.polygon(screen, fare.color, points)

# Function to draw revenue meters
def draw_revenue_meters(taxis):
    for i, taxi in enumerate(taxis):
        meter_x = METER_START_X
        meter_y = METER_START_Y + i * (METER_HEIGHT + METER_SPACING)
        pygame.draw.rect(screen, WHITE, (meter_x, meter_y, METER_WIDTH, METER_HEIGHT))
        font = pygame.font.Font(None, 24)
        text = font.render(f"Taxi {taxi.id}: £{taxi.total_earnings}, Fares: {taxi.total_fares}", True, BLACK)
        screen.blit(text, (meter_x, meter_y - 25))

# Function to add a new fare
def add_fare(junctions, streets, fares):
    src_junction = random.choice(junctions)
    dest_junction = random.choice(junctions)
    while src_junction == dest_junction:
        dest_junction = random.choice(junctions)
    fare = Fare(src_junction, dest_junction)
    fares.append(fare)

# Function to place parked cars on the streets
def place_parked_cars(junction_positions):
    parked_cars = []
    for pos in junction_positions:
        parked_cars.append(pos)
    return parked_cars
        
    return parked_cars
# Function to draw parked cars
def draw_parked_cars(parked_cars):
    for car in parked_cars:
        pygame.draw.rect(screen, BLUE, (OFFSET_X + car[0] * CELL_SIZE - 4, OFFSET_Y + car[1] * CELL_SIZE - 4, 8, 8))

def draw_dropped_off_fares(dropped_fares):
    for fare in dropped_fares:
        # Draw a blue triangle (cone) for dropped-off fares
        points = [
            (OFFSET_X + fare[0] * CELL_SIZE, OFFSET_Y + fare[1] * CELL_SIZE - 4),
            (OFFSET_X + fare[0] * CELL_SIZE - 4, OFFSET_Y + fare[1] * CELL_SIZE + 4),
            (OFFSET_X + fare[0] * CELL_SIZE + 4, OFFSET_Y + fare[1] * CELL_SIZE + 4)
        ]
        pygame.draw.polygon(screen, DROPPED_OFF_COLOR, points)

taxis = []
for i in range(4):  
    random_junction = random.choice(junctions)
    taxi_id = f"{i+1:03d}"  # Assign a unique ID (001, 002, ..., 008)
    taxi = Taxi(taxi_id, BLACK, random_junction.x, random_junction.y)
    taxis.append(taxi)
    networld.add_taxi(taxi)
    print(f"Taxi {taxi_id} placed at ({random_junction.x}, {random_junction.y})")

# Place initial fares randomly on the grid
# Place fares in the world
fares = networld.place_fares(NUM_FARES)

# Place parked cars randomly on the grid
# Define allowed positions for parked cars
allowed_positions = [(30, 15), (30, 30)]#(24, 35), (20, 0), (10, 24), (15, 15)]

# Place parked cars at the specific junctions
parked_cars = place_parked_cars(allowed_positions)

def bounded_model_checking(taxis, junctions, streets, parked_cars, N):
    solver = Solver()

    # Create variables for each taxi's position over the next N steps
    taxi_positions = {
        taxi.id: [(Int(f"x_{taxi.id}_{t}"), Int(f"y_{taxi.id}_{t}")) for t in range(N)]
        for taxi in taxis
    }

    # Add constraints for each taxi's movement
    for taxi in taxis:
        for t in range(N):
            if t == 0:
                # Current position constraint
                solver.add(taxi_positions[taxi.id][t][0] == taxi.x)
                solver.add(taxi_positions[taxi.id][t][1] == taxi.y)
            else:
                # Get possible next positions using the move logic
                current_position = (taxi.x, taxi.y)
                next_positions = taxi.get_adjacent_positions(current_position, streets)

                constraints = []
                for next_position in next_positions:
                    # Add a constraint to avoid parked cars
                    if next_position not in parked_cars:
                        constraints.append(And(
                            taxi_positions[taxi.id][t][0] == next_position[0],
                            taxi_positions[taxi.id][t][1] == next_position[1]
                        ))

                # the constraint that the taxi must move to one of the possible next positions
                if constraints:
                    solver.add(Or(*constraints))

    # collision avoidance constraints with safe distance
    for t in range(N):
        for taxi1_id, taxi2_id in combinations(taxi_positions.keys(), 2):
            x1, y1 = taxi_positions[taxi1_id][t]
            x2, y2 = taxi_positions[taxi2_id][t]
            
            # Calculate the Manhattan distance in Z3 terms
            distance_x = If(x1 >= x2, x1 - x2, x2 - x1)
            distance_y = If(y1 >= y2, y1 - y2, y2 - y1)
            
            # Ensure that taxis stay at least 1 grid unit away from each other (Manhattan distance)
            solver.add(distance_x + distance_y > 1)

    # Check if there is a solution that avoids collisions and parked cars
    if solver.check() == sat:
        model = solver.model()
        for taxi in taxis:
            next_x = model[taxi_positions[taxi.id][1][0]].as_long()
            next_y = model[taxi_positions[taxi.id][1][1]].as_long()
            taxi.x, taxi.y = next_x, next_y
    else:
        print("Collision or blocked path detected within the next steps!")



# simulation time limit (in seconds)
SIMULATION_TIME_LIMIT = 5 * 60  # 5 minutes
# tracking memory allocations
tracemalloc.start()
total_fares_picked = 0
frame_count = 0
# Track the number of dropped-off fares
total_fares_completed = 0  
running = True
start_time = time.time()
# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for collisions and move taxis safely
    bounded_model_checking(taxis, junctions, streets, parked_cars, N=3)

    all_fares_handled = True

    # After taxis move, check if any can pick up or drop off fares
    for taxi in taxis:
        if taxi.has_fare:
            # Check if the taxi is at the fare's destination
            if taxi.x == taxi.current_fare.destination.x and taxi.y == taxi.current_fare.destination.y:
                drop_off_location = (taxi.x, taxi.y)
                taxi.drop_off_fare()  # Drop off the fare
                taxi.color = BLACK
                dropped_off_fares.append(drop_off_location)
                total_fares_completed += 1  # Increment the completed fare count
                print(f"Taxi {taxi.id} dropped off fare at ({taxi.x}, {taxi.y}). Total earnings: £{taxi.total_earnings}")
        else:
            if fares:
                all_fares_handled = False  # There are still fares to be picked up
                # Check if taxi is at the fare's origin
                for fare in fares[:]:  # Iterate over a copy of the list to allow removal
                    if taxi.x == fare.origin.x and taxi.y == fare.origin.y:
                        taxi.pick_up_fare(fare, fares)  # Pass both fare and fares list
                        taxi.color = RED
                        total_fares_picked += 1
                        print(f"Taxi {taxi.id} picked up a fare to ({fare.destination.x}, {fare.destination.y})")
                        break

    # Add new fares at intervals (e.g., every 5 seconds)
    if frame_count % (5 * 30) == 0:  # Assuming 30 frames per second
        add_fare(junctions, streets, fares)

    # Check if the simulation time limit has been reached
    elapsed_time = time.time() - start_time
    if elapsed_time >= 300:  # 5 minutes in seconds
        print("Time limit reached. Ending simulation.")
        running = False

    # If all fares have been picked up and dropped off, end the simulation
    if not fares and all(not taxi.has_fare for taxi in taxis):
        running = False
        print("All fares have been handled and dropped off. Simulation ending.")

    screen.fill(WHITE)

    # Draw the streets, junctions, taxis, fares, and parked cars
    draw_streets()
    draw_junctions()
    draw_taxis(taxis)
    draw_fares(fares, parked_cars)
    draw_dropped_off_fares(dropped_off_fares)
    draw_revenue_meters(taxis)
    draw_parked_cars(parked_cars)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to slow down the simulation
    pygame.time.Clock().tick(30)
    time.sleep(0.001)

    frame_count += 1

# Stop tracking memory allocations
current, peak = tracemalloc.get_traced_memory()

# Print the total earnings for each taxi
print("\nTotal earnings for each taxi:")
for taxi in taxis:
    print(f"Taxi {taxi.id} earned £{taxi.total_earnings} and picked up {taxi.total_fares} fares.")

# Calculate and print the total revenue
total_revenue = total_fares_completed * 10
print(f"Total revenue: £{total_revenue}")
print(f"Total picked fares: {total_fares_picked}")
# Print memory usage
print(f"Current memory usage: {current / 10**6} MB")
print(f"Peak memory usage: {peak / 10**6} MB")

# Quit Pygame
pygame.quit()
sys.exit()

