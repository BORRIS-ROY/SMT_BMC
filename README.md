# SMT_BMC
The project is a detailed simulation framework designed to model the operations of autono
mous taxis within a dynamic, grid-based urban environment. The primary focus is on the naviga
tion of taxis through a city grid, where they provide transportation services while avoiding obsta
cles, optimizing efficiency and maintaining safety. The simulation incorporates elements of arti
ficial intelligence, specifically pathfinding algorithms such as Breadth-First Search (BFS) and 
utilises model checking techniques to ensure that the taxis operate safely and efficiently. 

1. Auto1.py: Contains the main simulation loop for the taxi system. It manages the move
ment of taxis, fare handling, and the drawing of simulation elements (junctions, streets, 
taxis, and fares) on the screen. It handles the core simulation mechanics and display 
updates. 
2. Junc1.py: This module defines and manages the junctions, and streets. It contains the 
logic for creating and managing junctions, including attributes like coordinates and the 
connections between junctions and streets. 
3. Tax.py: This manages individual taxis in the simulation, including their movement, path
finding (A*, BFS and DFS algorithms), fare handling and interactions with junctions and 
streets. 
4. NetWorld.py: Contains high level simulation world logic, including placing fares, 
streets, and managing the interactions between different entities (taxis, streets, junc
tions, and obstacles/buildings).

# The Constraints 
1. Collision Avoidance: Taxis can not occupy the same grid position at the same time. 
2. Obstacle Avoidance: Taxis must avoid collisions or spaces occupied by the obstacles (parked 
cars) 
3. Traffic Regulations: Taxis must leave a specified gap between themselves. 
