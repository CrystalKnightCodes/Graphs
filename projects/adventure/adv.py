from room import Room
from player import Player
from world import World
from ast import literal_eval
import collections
import random

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

def explore(player, max_rooms): 
    travel_path = []
    pending = collections.deque()
    traversed = {}
    entry = {}

    def find_path():
        room = player.current_room
        exits = room.get_exits()
        
        for direction in exits:
            neighbor = room.get_room_in_direction(direction)
            if neighbor.id in traversed:
                entry[direction] = neighbor.id 
            else:
                entry[direction] = '?'
                forward = (room.id, direction)
                if forward not in pending:
                    backtrack = (neighbor.id, get_opposite_direction(direction))
                    pending.append(backtrack)
                    pending.append((forward))

        traversed[room.id] = entry

        if len(pending) > 0:
            travel_entry = pending.pop()
            travel_direction = travel_entry[1]
            travel_path.append(travel_direction)
            player.travel(travel_direction)
            previous_room_id = travel_entry[0]
            traversed[previous_room_id][travel_direction] = room.id
        else:
            new_direction = get_random_direction(exits)
            travel_path.append(travel_direction)
            player.travel(new_direction)
            
    while len(traversed) < max_rooms:
        find_path()
    return travel_path

def get_random_direction(exits):

    return random.choice(exits)

def get_opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "e":
        return "w"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    else:
        raise "Invalid Direction"

traversal_path = explore(player, len(room_graph))
print(f"Traversal path: {traversal_path}")

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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
