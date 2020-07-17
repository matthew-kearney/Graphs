from room import Room
from player import Player
from world import World
from utilities import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []

# NOTES
'''
figure out how the rooms are connected and which ones are connected together
so check rooms connected to the starting room then recursivly map the graph until all rooms
are visited 
'''

def room_recursive(starting_room,room_graph,room_paths=None,visited=None):
    
    # FOR: how rooms are connected together.
    # NOTES
    # starting_room = node evaluating neighbors of cur room
    # room_graph = gen world we are eploring
    # room_paths = The linked paths that a room can lead to, default value of None. per room during R
    # visited = The list of rooms that have been visited 
    
    #no room has been visited create empty list
    if visited is None:
        visited = []
    # create a set for room paths
    if room_paths is None:
        room_paths = {}
    #declare the current room's ID
    room_id = starting_room.id

    # if not in the room path add room id to visited list
    if room_id not in room_paths.keys():
        visited.append(room_id)
        #in the pathing dictionary
        #add this room as a key
        room_paths[room_id] = {}
        #make directions for that starting room.
        directions = starting_room.get_exits()
        
        for dir in directions:
            #update path dict at the key of the room ID
            #attach direction, and ID of connected room
            room_paths[room_id].update({dir:starting_room.get_room_in_direction(dir).id})
        #shuffle the directions a room has to have
        directions = starting_room.get_exits()
        random.shuffle(directions)
        #for all rooms that have a room or more not visited vistit it
        for direction in directions:
            new_room = starting_room.get_room_in_direction(direction)
            #recursively apply the same logic for the next room and so on
            room_recursive(new_room,room_graph,room_paths,visited)
        if len(room_paths) == len(room_graph):
            return room_paths,visited
        
def bfs(starting_room, next_room,room_paths):
    
    # breadth first search
    # for the shortest path of starting room to next room
    # NOTES
    # startingroom - id visa versa for next room
    
    visited = set()
    room_queue = Queue()
    dir_queue = Queue()
    room_queue.enqueue([starting_room])
    dir_queue.enqueue([])
    
    


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
