import curses
import random

def create_grid(n):
    return [[" " for _ in range(n)] for _ in range(n)]

def mark_path(grid, path):
    for x, y in path:
        grid[x][y] = "X"

def carve_path(grid, x, y, visited, target_x, target_y):
    visited.add((x, y))
    if x == target_x and y == target_y:
        return
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # All four directions
    random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = x + 2*dx, y + 2*dy
        mid_x, mid_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            if (new_x, new_y) not in visited:
                grid[new_x][new_y] = "X"
                grid[mid_x][mid_y] = "X"
                carve_path(grid, new_x, new_y, visited, target_x, target_y)

def draw_grid(stdscr, grid, player_x, player_y):
    stdscr.clear()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if i == player_x and j == player_y:
                stdscr.addstr(i, j*2, "@")  # Player character
            else:
                stdscr.addstr(i, j*2, cell)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    grid_size = 9
    grid = create_grid(grid_size)
    start_x, start_y = 0, 0
    end_x, end_y = grid_size - 1, grid_size - 1
    visited = {(start_x, start_y)}

    # Mark the start cell before carving the path
    grid[start_x][start_y] = "[X]"

    carve_path(grid, start_x, start_y, visited, end_x, end_y)

    player_x, player_y = start_x, start_y
    while True:
        draw_grid(stdscr, grid, player_x, player_y)
        key = stdscr.getch()

        if key == curses.KEY_UP and player_x > 0 and grid[player_x - 1][player_y] == "[X]":
            player_x -= 1
        elif key == curses.KEY_DOWN and player_x < grid_size - 1 and grid[player_x + 1][player_y] == "[X]":
            player_x += 1
        elif key == curses.KEY_LEFT and player_y > 0 and grid[player_y - 1][player_x] == "[X]":
            player_y -= 1
        elif key == curses.KEY_RIGHT and player_y < grid_size - 1 and grid[player_y + 1][player_x] == "[X]":
            player_y += 1
        elif key == ord('q'):  # Quit the game
            break

if __name__ == "__main__":
    curses.wrapper(main)