# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
from random import randint

class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        return_str = ""
        return_str += f"Room No {self.id} ({self.x}, {self.y})\n"
        if self.e_to is not None:
             return_str += f"({self.x}, {self.y}) east -> ({self.e_to.x}, {self.e_to.y})\n"
        if self.w_to is not None:
            return_str += f"({self.x}, {self.y}) west -> ({self.w_to.x}, {self.w_to.y})\n"
        if self.n_to is not None:
            return_str += f"({self.x}, {self.y}) north -> ({self.n_to.x}, {self.n_to.y})\n"
        if self.s_to is not None:
            return_str += f"({self.x}, {self.y}) south -> ({self.s_to.x}, {self.s_to.y})\n"
        
        return return_str
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 12
        self.height = 12
        self.rooms = []

    def is_in_grid(self, direction, x, y):
        if direction == 'w':
            return self.grid[y][x - 1]
        elif direction == 'n':
            return self.grid[y + 1][x]
        elif direction == 'e':
            return self.grid[y][x + 1]

    def is_out_of_bounds(self, direction, x, y):
        if direction == 'w':
            return (x - 1) < 0
        elif direction == 'n':
            return (y + 1) >= self.height
        elif direction == 'e':
            return (x + 1) >= self.width

    def generate_rooms(self):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * self.height
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * self.width

        # start from middle of the bottom row
        seed_x = self.width // 2
        seed_y = 0

        x = seed_x
        y = seed_y
        room_count = 0
        # seed the first room
        seed_room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
        self.rooms.append(seed_room)
        self.grid[y][x] = seed_room
        room_count += 1

        # While there are rooms to be created...
        while room_count < 100:
            # never travel south
            directions = ['w', 'n', 'e']
            prev_direction = None

            # start at the seed room
            previous_room = seed_room

            # reset x and y coordinates
            x = seed_x
            y = seed_y

            # find a random direction
            direction = directions[randint(0, 2)]

            can_move = True

            # traverse rooms...
            while can_move == True:
                # if no room in grid
                if not self.is_out_of_bounds(direction, x, y) and self.is_in_grid(direction, x, y) is None:
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1

                    # Create a room in the given direction
                    room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
                    # Note that in Django, you'll need to save the room after you create it    
                    self.rooms.append(room)


                    # Save the room in the World grid
                    self.grid[y][x] = room

                    # Connect the new room to the previous room
                    previous_room.connect_rooms(room, direction)

                    # Update iteration variables
                    room_count += 1

                    can_move = False
                # if room in grid and prev room is connected to target room,
                elif previous_room.get_room_in_direction(direction) is not None:
                    # move to that room
                    previous_room = previous_room.get_room_in_direction(direction)
                    
                    # update coordinate value
                    if direction == 'w':
                        x -= 1
                    elif direction == 'n':
                        y += 1
                    elif direction == 'e':
                        x += 1

                    # find a new random direction
                    prev_direction = direction
                    directions = ['w', 'n', 'e']
                    direction = directions[randint(0, 2)]
                # if room is outside bounds OR if room in grid and prev room not connected to target room
                elif self.is_out_of_bounds(direction, x, y) or previous_room.get_room_in_direction(direction) is None:
                    # if no directions available
                    if directions == None:
                        can_move = False
                    # try again in available directions
                    elif len(directions) == 3:
                        if prev_direction == 'e':
                            directions = ['n', 'e']
                            direction = 'n'
                        elif prev_direction == 'w':
                            directions = ['n', 'w']
                            direction = 'n'
                        elif prev_direction == 'n':
                            directions = ['w', 'e']
                            direction = 'w'
                    elif len(directions) == 2:
                        if prev_direction == 'e':
                            direction = 'e'
                        elif prev_direction == 'w':
                            direction = 'w'
                        elif prev_direction == 'n':
                            direction = 'e'
                        directions = None


            # update coordinate value
            # if direction == 'w':
            #     x -= 1
            # elif direction == 'n':
            #     y += 1
            # elif direction == 'e':
            #     x += 1



    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        for room in self.rooms:
            print(room)

        # # Add top border
        # str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # # The console prints top to bottom but our array is arranged
        # # bottom to top.
        # #
        # # We reverse it so it draws in the right direction.
        # reverse_grid = list(self.grid) # make a copy of the list
        # reverse_grid.reverse()
        # for row in reverse_grid:
        #     # PRINT NORTH CONNECTION ROW
        #     str += "#"
        #     for room in row:
        #         if room is not None and room.n_to is not None:
        #             str += "  |  "
        #         else:
        #             str += "     "
        #     str += "#\n"
        #     # PRINT ROOM ROW
        #     str += "#"
        #     for room in row:
        #         if room is not None and room.w_to is not None:
        #             str += "-"
        #         else:
        #             str += " "
        #         if room is not None:
        #             str += f"{room.id}".zfill(3)
        #         else:
        #             str += "   "
        #         if room is not None and room.e_to is not None:
        #             str += "-"
        #         else:
        #             str += " "
        #     str += "#\n"
        #     # PRINT SOUTH CONNECTION ROW
        #     str += "#"
        #     for room in row:
        #         if room is not None and room.s_to is not None:
        #             str += "  |  "
        #         else:
        #             str += "     "
        #     str += "#\n"

        # # Add bottom border
        # str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # # Print string
        # print(str)


w = World()
num_rooms = 100
width = 10
height = 12
w.generate_rooms()
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
