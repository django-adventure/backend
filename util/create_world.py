# paste into shell in sections:
# **************************************************************************
from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import randint, shuffle
Room.objects.all().delete()
adj = ["Irradiated", "Gloomy", "Deserted", "Ominous", "Bleak", "Cold", "Secure", "Eerie", "Desolate", "Deadly"]
nouns = [
    ["Bunker", "You break into a sturdy concrete bunker. Could there be something stashed away?"], 
    ["Ruin", "Twisted bits of metal poke out of the unrecognizable burnt wreckage. You might find something to salvage."], 
    ["Cave", "A dark narrow passage leads to a large humid cave filled with stalactites and stalagmites. You forget which one is which."], 
    ["Hills", "Scattered shrubs cover the hills before you."], 
    ["Desert", "Piles of sand stretch ahead for miles. "], 
    ["Graveyard", "A thick fog covers the crumbling tombstones. You feel a chill run down your spine."], 
    ["Base", "A rusty fence surrounds clusters of makeshift buildings and vehicles."], 
    ["Depot", "A maze of dusty shelves littered with junk. Most everything has been looted."], 
    ["Sewer", "Large tunnels span in several directions. It smells horrible in here."], 
    ["Town", "One lone building stands in the remnants of a town. If only there was someone to talk to."],
    ]
rooms = []
descriptions = []
items = [
    {'name': 'chicken', 'description': 'Friend or food?'},
    {'name': 'rope', 'description': 'Good for climbing'},
    {'name': 'matches', 'description': 'A little soggy'},
    {'name': 'crowbar', 'description': 'A handy all-purpose tool'},
    {'name': 'cloak', 'description': 'Shield yourself from your enemies'},
    {'name': 'goo', 'description': 'Strange and glowing'},
    {'name': 'doubloon', 'description': 'A beautiful gold coin'},
    {'name': 'batteries', 'description': 'AA, AAA, and AAAAAAAAA'},
    {'name': 'bitcoin', 'description': 'How did I pick this up?'},
    {'name': 'lighter', 'description': 'It\'s lit'},
    {'name': 'bat-on-a-stick', 'description': 'Virus free!'},
    {'name': 'donut', 'description': 'It\'s chocolate flavored. Jeff already took a bite.'},
]
# **************************************************************************
# counter = 0
# for r in all_rooms:
#     r.title = rooms[counter]
#     r.description = descriptions[counter]
#     r.save()
#     counter += 1
all_items=[]
for i in items:
    new_item = Item(name=i['name'], description=i['description'])
    all_items.append(new_item)
    new_item.save()
counter = 0
for r in all_rooms:
    if counter % 2 == 0:
        i = randint(0, 11)
        r.items.add(all_items[i])
    if counter % 3 == 0:
        i = randint(0, 11)
        r.items.add(all_items[i])
    if counter % 5 == 0:
        i = randint(0, 11)
        r.items.add(all_items[i])
    counter += 1
# **************************************************************************
for i in range(len(adj)):
    for j in range(len(adj)):
        rooms.append(adj[i] + " " + nouns[j][0])
# **************************************************************************
vowels = ['A', 'E', 'I', 'O', 'U']
for i in range(len(adj)):
    for j in range(len(adj)): 
        if adj[i][0] in vowels:
            descriptions.append(f"{nouns[j][1]} It gives you an {adj[i].lower()} feeling.")
        else:
            descriptions.append(f"{nouns[j][1]} It gives you a {adj[i].lower()} feeling.")
# **************************************************************************
class World:
    def __init__(self):
        self.grid = None
        self.width = 12
        self.height = 12
    def is_in_grid(self, direction, x, y):
        if direction == 'w':
            return self.grid[y][x - 1]
        elif direction == 'n':
            return self.grid[y + 1][x]
        elif direction == 'e':
            return self.grid[y][x + 1]
        elif direction == 's':
            return self.grid[y - 1][x]
    def is_out_of_bounds(self, direction, x, y):
        if direction == 'w':
            return (x - 1) < 0
        elif direction == 'n':
            return (y + 1) >= self.height
        elif direction == 'e':
            return (x + 1) >= self.width
        elif direction == 's':
            return (y - 1) < 0
    def generate_rooms(self):
        # Initialize the grid
        self.grid = [None] * self.height
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * self.width
        # start from middle of the bottom row
        seed_x = self.width // 2
        seed_y = self.height // 2
        x = seed_x
        y = seed_y
        room_count = 0
        # seed the first room
        seed_room = Room(title=rooms[0], description=descriptions[0], x=x, y=y)
        seed_room.save()
        self.grid[y][x] = seed_room
        room_count += 1
        # start players in seed room
        players = Player.objects.all()
        for p in players:
            p.currentRoom=seed_room.id
            p.save()
        # While there are rooms to be created...
        while room_count < 100:
            # never travel south
            directions = ['w', 'n', 'e', 's']
            prev_direction = None
            # start at the seed room
            previous_room = seed_room.id
            # reset x and y coordinates
            x = seed_x
            y = seed_y
            # find a random direction
            direction = directions[randint(0, 3)]
            can_move = True
            # traverse rooms...
            while can_move == True:
                # if no room in grid
                print(room_count)
                if not self.is_out_of_bounds(direction, x, y) and self.is_in_grid(direction, x, y) is None:
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1
                    elif direction == 's':
                        y -= 1
                    # Create a room in the given direction
                    room = Room(title=rooms[room_count], description=descriptions[room_count], x=x, y=y)
                    # save room 
                    room.save()
                    # Save the room in the World grid
                    self.grid[y][x] = room
                    # Connect the new room to the previous room
                    # previous_room.connectRooms(room, direction)
                    Room.objects.get(id=previous_room).connectRooms(room, direction)
                    # Update iteration variables
                    room_count += 1
                    can_move = False
                # if room in grid and prev room is connected to target room,
                # elif previous_room.getRoomInDirection(direction) != 0:
                elif getattr(Room.objects.get(id=previous_room), f"{direction}_to") != 0:
                    # move to that room
                    # previous_room = getattr(previous_room, f"{direction}_to")
                    previous_room = getattr(Room.objects.get(id=previous_room), f"{direction}_to")
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1
                    elif direction == 's':
                        y -= 1
                    # find a new random direction
                    prev_direction = direction
                    if prev_direction == 'e':
                        directions = ['n', 'e', 's']
                    elif prev_direction == 'w':
                        directions = ['s', 'n', 'w']
                    elif prev_direction == 'n':
                        directions = ['e', 'w', 'n']
                    elif prev_direction == 's':
                        directions = ['w', 's', 'e']
                    direction = directions[randint(0, 2)]
                # if room is outside bounds OR if room in grid and prev room not connected to target room
                elif self.is_out_of_bounds(direction, x, y) or getattr(Room.objects.get(id=previous_room), f"{direction}_to") == 0:
                    # if no directions available
                    if directions == None:
                        can_move = False
                    # try again in available directions
                    elif len(directions) == 4:
                        if prev_direction == 'e':
                            directions = ['n', 'e', 's']
                            direction = 'n'
                        elif prev_direction == 'w':
                            directions = ['s', 'n', 'w']
                            direction = 's'
                        elif prev_direction == 'n':
                            directions = ['e', 'w', 'n']
                            direction = 'e'
                        elif prev_direction == 's':
                            directions = ['w', 's', 'e']
                            direction = 'w'
                    elif len(directions) == 3:
                        if prev_direction == 'e':
                            directions = ['e', 's']
                            direction = 'e'
                        elif prev_direction == 'w':
                            directions = ['n', 'w']
                            direction = 'n'
                        elif prev_direction == 'n':
                            directions = ['w', 'n']
                            direction = 'w'
                        elif prev_direction == 's':
                            directions = ['s', 'e']
                            direction = 's'
                    elif len(directions) == 2:
                        if prev_direction == 'e':
                            direction = 's'
                        elif prev_direction == 'w':
                            direction = 'w'
                        elif prev_direction == 'n':
                            direction = 'n'
                        elif prev_direction == 's':
                            direction = 'e'
                        directions = None
# **************************************************************************
World().generate_rooms()
