import curses
import random
import os
import copy

class Room:
    def __init__(self, description, loot=None, doors=None, location=None):
        self.description = description
        self.loot = loot
        self.neighbors = {}
        self.doors = {}
        self.location = location  # Add location attribute to store coordinates

    def add_neighbor(self, direction, neighbor):
        self.neighbors[direction] = neighbor
        
    def has_neighbor(self,direction):
        return direction in self.neighbors
    
    def add_door(self,direction):
        self.doors[direction] = True
        
    def has_door(self,direction):
        return direction in self.doors


# define player character
class Player:
    def __init__(self, start_location):
        self.location = start_location
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)


def explore_room(stdscr, room, player, explored_rooms):
    stdscr.erase()  # Clear the entire screen before printing updated content
    stdscr.addstr(0, 0, 'Use arrow keys to move (press \'q\' to quit)')
    stdscr.addstr(1, 0, room.description)  # Print the room description
    if room.loot:
        stdscr.addstr(2, 0, 'You found some loot: ' + room.loot)  # Print loot if present
    if room.doors:
        stdscr.addstr(3, 0, 'Doors in this room: ' + ', '.join(room.doors))  # Print doors if present

    # Print explored, neighboring, and current rooms
    for i, row in enumerate(explored_rooms):
        for j, room_explored in enumerate(row):
            symbol = '[ ]'  # Default symbol for unexplored rooms
            if room_explored:
                if [i, j] == player.location:
                    symbol = '[.]'  # Symbol for current room
                else:
                    symbol = '[X]'  # Symbol for explored room
            elif room.has_neighbor((i, j)):
                symbol = '[ ]'  # Empty space for neighboring rooms without doors
                # Check if there's a door to the neighboring room
                neighbor = room.neighbors.get((i, j))
                if neighbor and room.has_door((i, j)):
                    symbol = '[D]'  # Symbol for neighboring room with a door
            stdscr.addstr(i + 5, j * 3, symbol)

    stdscr.refresh()  # Refresh the screen




def move(stdscr, player, direction, rooms, explored_rooms):
    current_room = rooms[player.location[0]][player.location[1]]
    neighbor_room = current_room.neighbors.get(direction)
    
    if neighbor_room is not None and current_room.has_door(direction):  # Check if there is a door in the specified direction
        new_location = neighbor_room.location  # Retrieve coordinates of the neighboring room
        if isinstance(new_location, list) and len(new_location) == 2:
            new_row, new_col = new_location
            if 0 <= new_row < len(rooms) and 0 <= new_col < len(rooms[0]):
                explore_room(stdscr, neighbor_room, player, explored_rooms)  # Explore the neighboring room
                stdscr.refresh()  # Refresh the screen after exploring the new room
                explored_rooms[new_row][new_col] = True  # Mark the new room as explored
                player.location = new_location  # Move the player to the new location
                return True, new_location, None  # Return success and new location
    # If there's no neighbor room or no door in the specified direction, return failure with an error code
    return False, None, 'No path in that direction'


directions = ['north', 'south', 'east', 'west']



def generate_rooms(num_rows, num_cols, descriptions, loot, room_density=0.5):
    rooms = [[None for _ in range(num_cols)] for _ in range(num_rows)]
    available_spaces = [(i, j) for i in range(num_rows) for j in range(num_cols)]

    while available_spaces:
        i, j = available_spaces.pop(random.randrange(len(available_spaces)))
        if random.random() < room_density:
            description = descriptions.pop()
            room_loot = loot.pop() if random.random() < 0.7 else None
            room = Room('You are in a ' + description + '.', room_loot, location=[i, j])
            rooms[i][j] = room
            # Connect the room to at least one neighboring room
            connected = False
            random.shuffle(directions)
            for direction in directions:
                if direction == 'north' and i > 0 and rooms[i - 1][j] is not None:
                    room.add_neighbor('north', rooms[i - 1][j])
                    rooms[i - 1][j].add_neighbor('south', room)
                    connected = True
                    break
                elif direction == 'south' and i < num_rows - 1 and rooms[i + 1][j] is not None:
                    room.add_neighbor('south', rooms[i + 1][j])
                    rooms[i + 1][j].add_neighbor('north', room)
                    connected = True
                    break
                elif direction == 'west' and j > 0 and rooms[i][j - 1] is not None:
                    room.add_neighbor('west', rooms[i][j - 1])
                    rooms[i][j - 1].add_neighbor('east', room)
                    connected = True
                    break
                elif direction == 'east' and j < num_cols - 1 and rooms[i][j + 1] is not None:
                    room.add_neighbor('east', rooms[i][j + 1])
                    rooms[i][j + 1].add_neighbor('west', room)
                    connected = True
                    break
    return rooms




import random

def assign_neighbors(rooms):
    num_rows = len(rooms)
    num_cols = len(rooms[0])
    
    for i in range(num_rows):
        for j in range(num_cols):
            room = rooms[i][j]
            if room is not None:  # Ensure room is not None
                valid_directions = []
                if i > 0 and rooms[i - 1][j] is not None:
                    valid_directions.append('north')
                if i < num_rows - 1 and rooms[i + 1][j] is not None:
                    valid_directions.append('south')
                if j > 0 and rooms[i][j - 1] is not None:
                    valid_directions.append('west')
                if j < num_cols - 1 and rooms[i][j + 1] is not None:
                    valid_directions.append('east')

                for direction in valid_directions:
                    neighbor = None
                    if direction == 'north':
                        neighbor = rooms[i - 1][j]
                    elif direction == 'south':
                        neighbor = rooms[i + 1][j]
                    elif direction == 'west':
                        neighbor = rooms[i][j - 1]
                    elif direction == 'east':
                        neighbor = rooms[i][j + 1]
                    
                    if neighbor is not None:  # Ensure neighbor is not None
                        room.add_neighbor(direction, neighbor)
                        neighbor.add_neighbor(opposite_direction(direction), room)
                        room.add_door(direction)
                        neighbor.add_door(opposite_direction(direction))

    return rooms

def opposite_direction(direction):
    if direction == 'north':
        return 'south'
    elif direction == 'south':
        return 'north'
    elif direction == 'west':
        return 'east'
    elif direction == 'east':
        return 'west'






descriptions = ['dark cave', 'spooky graveyard', 'treasure room',
                'dark forest', 'mysterious temple', 'haunted mansion',
                'deserted beach', 'hidden underground passage', 'lush garden',
                'spooky attic', 'dank basement', 'old warehouse', 'abandoned mineshaft',
                'old mineshaft', 'abandoned warehouse','bomb shelter', 'police station'
               ]
loot = ['Gold coin', 'Health potion', 'Magic sword', 'Silver dagger', 'magic wand', 'pebble',
        'Gold coin', 'Gold coin', 'Gold coin', 'worthless pebble', 'worthless pebble', 'worthless pebble',
        'Ancient artifact', 'Glowing crystal', 'Pearl necklace', 'Enchanted book', 'Rare flower']

# Shuffle descriptions, loot, and directions
random.shuffle(descriptions)
random.shuffle(loot)


def get_input(stdscr):
    key = stdscr.getch() 
    return key

def main(stdscr):
    # Ensure that the program doesn't wait for the Enter key to be pressed
    curses.cbreak()
    # Disable cursor visibility
    curses.curs_set(0)
    # Clear the screen
    stdscr.clear()

    start_location = [0,0]
    # print('Initial player's location:', player.location)

    player = Player(start_location)
    num_rows = 5
    num_cols = 5

    rooms = generate_rooms(num_rows,num_cols,descriptions,loot)
    rooms = assign_neighbors(rooms)


    # Initialize explored rooms
    explored_rooms = [[False for _ in range(num_cols)] for _ in range(num_rows)]
    explored_rooms[start_location[0]][start_location[1]] = True

    while True:
        # Print player's location coordinates for debugging
        print("Player's location:", player.location)
        # Check if the corresponding room exists in the rooms list
        if rooms[player.location[0]][player.location[1]] is not None:
            room = rooms[player.location[0]][player.location[1]]
            explore_room(stdscr, room, player, explored_rooms)
        else:
            print("Error: Room at player's location is None")
        key = get_input(stdscr)
        # print('Pressed key:', key)
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_LEFT]:
            new_location = copy.copy(player.location)
            if key == curses.KEY_UP or key == ord('w'):
                move_direction = 'north'
                new_location = [player.location[0] - 1, player.location[1]]
            elif key == curses.KEY_DOWN or key == ord('s'):
                move_direction = 'south'
                new_location = [player.location[0] + 1, player.location[1]]
            elif key == curses.KEY_RIGHT or key == ord('d'):
                move_direction = 'east'
                new_location = [player.location[0], player.location[1] + 1]
            elif key == curses.KEY_LEFT or key == ord('a'):
                move_direction = 'west'
                new_location = [player.location[0], player.location[1] - 1]

            if 0 <= new_location[0] < num_rows and 0 <= new_location[1] < num_cols:
                available_directions = rooms[player.location[0]][player.location[1]].neighbors.keys()
                if move_direction in available_directions:
                    success, new_location, error_message = move(stdscr, player, move_direction, rooms, explored_rooms)
                    if success:
                        explore_room(stdscr, rooms[new_location[0]][new_location[1]], player, explored_rooms)
                else:
                    stdscr.addstr(10, 0, 'No path in that direction')  # Display error message
                    stdscr.refresh()  # Refresh the screen after displaying the error message
        elif key == ord('q'):
            break
        else:
            stdscr.addstr(10, 0, 'Invalid key')  # Display error message for invalid key
            stdscr.refresh()  # Refresh the screen after displaying the error message



    

    # End curses window
    curses.endwin()
if __name__ == '__main__':
    curses.wrapper(main)
