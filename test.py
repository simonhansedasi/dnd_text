import colorama
from colorama import Fore, Style
import random

colorama.init()

def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()

def create_grid(n):
    return [["[ ]" for _ in range(n)] for _ in range(n)]

def mark_path(grid, path):
    for x, y in path:
        grid[x][y] = f"[{Fore.GREEN}X{Style.RESET_ALL}]"

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
                grid[new_x][new_y] = f"[{Fore.GREEN}X{Style.RESET_ALL}]"
                if dx != 0:
                    grid[mid_x][y] = f"[{Fore.GREEN}X{Style.RESET_ALL}]"
                elif dy != 0:
                    grid[x][mid_y] = f"[{Fore.GREEN}X{Style.RESET_ALL}]"
                carve_path(grid, new_x, new_y, visited, target_x, target_y)

if __name__ == "__main__":
    grid_size = 9
    grid = create_grid(grid_size)
    start_x, start_y = 0, 0
    end_x, end_y = grid_size - 1, grid_size - 1
    visited = {(start_x, start_y)}

    # Marking the start cell before carving the path
    grid[start_x][start_y] = f"[{Fore.GREEN}X{Style.RESET_ALL}]"

    carve_path(grid, start_x, start_y, visited, end_x, end_y)
    print_grid(grid)