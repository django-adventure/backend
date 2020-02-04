from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import randint, shuffle
Room.objects.all().delete()
adj = ["Sunny", "Gloomy", "Happy", "Scary", "Fun", "Cold", "Fiery", "Lonely", "Boring", "Deadly"]
nouns = ["Desert", "Plateau", "Savannah", "Forest", "Tundra", "Taiga", "Iceberg", "Lake", "River", "Peak"]
rooms = []
descriptions = []
for i in range(len(adj)):
    for j in range(len(adj)):
        rooms.append(adj[i] + " " + nouns[j])
for i in range(len(adj)):
    for j in range(len(adj)): 
        if (i/2 == 0):
            descriptions.append(f"You are now in the {nouns[j]}. It is {adj[i]}. Keep moving to keep exploring!")
        else: 
            descriptions.append(f"This is the {nouns[j]}. It is {adj[i]}! What may await in the next room?")
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

# copy all lines of code above and paste into interpreter
# then run these two lines:
w = World()
w.generate_rooms()
