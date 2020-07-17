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
    
    # create lsit of vistited helps bfs run faster 
    visited = set()
    # queue to explore room order
    # bfs bc first in first out
    room_queue = Queue()
    # to queue the direction travel
    dir_queue = Queue()
    
    # queue start at starting room
    room_queue.enqueue([starting_room])
    # blank bc havent moved yet
    dir_queue.enqueue([])
    
    # while there are rooms in queue
    while room_queue.size() > 0:
        # gets next value in queue
        vertex_path = room_queue.dequeue()
        # gets next direcetion to travel in queue
        dir_path = dir_queue.dequeue()
        # last room in room_path taken from queue(newest explored room)
        vertex = vertex_path[-1]
        # if not vistited add vertex
        if vertex not in visited:
            visited.add(vertex)
            # if that new room is the right path
            if vertex == next_room:
                return dir_path
            # for each direction a room has mapped to it in the room_path dict
            for direction in room_paths[vertex]:
                # copy both queues
                path_copy = vertex_path.copy()
                dirpath_copy = dir_path.copy()
                # adding the newest room and direction to the copied room_path route 
                path_copy.append(room_paths[vertex][direction])
                dirpath_copy.append(direction)
                room_queue.enqueue(path_copy)
                dir_queue.enqueue(dirpath_copy)

# create anser list of TP
traversal_path = []
# set player in starting room
player = Player(world.starting_room)
# use recursion func to visit all rooms
room_dict,visited = room_recursive(world.starting_room,room_graph)

# for each room in the visit list 
# set path as the shortest pathway between two rooms
# add path of the nav between two rooms to the TP list 
for i in range(len(visited)-1):
    path = bfs(visited[i],visited[i+1],room_dict)
    traversal_path.extend(path)
    
    


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
