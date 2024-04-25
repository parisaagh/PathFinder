import tkinter as tk
from tkinter import filedialog
from collections import deque
import heapq
import cv2
import time
import random
import sys

# Global variables
root = None
canvas = None
hospital_map = None
cell_size = 4
delay = 5  # Delay in milliseconds (500 ms = 0.5 seconds)
start_location = None
PRIORITIES = None
output = []  # the success and failure output


# Helper functions
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    path = deque()
    while current in came_from:
        path.appendleft(current)
        current = came_from[current]
    path.appendleft(current)
    return list(path)


##########-----parisa-----##########
# A* algorithm
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found

##########-----Adrienne-----##########
# Dijkstra's algorithm
def dijkstra(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (tentative_g_score, neighbor))

    return []  # No path found


##########-----parisa-----##########
def get_neighbors(node):
    neighbors = []
    row, col = node
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(hospital_map) and 0 <= new_col < len(hospital_map[0]) and hospital_map[new_row][
            new_col] == 0:
            neighbors.append((new_row, new_col))

    return neighbors


##########-----Adrienne-----##########
def process_requests(start, algorithm, requests):
    paths = []
    priority_queue = []
    visited = set()
    start_location = tuple(start)

    for request in requests:
        row, col = request.split(',')
        location = (int(row), int(col))
        priority = PRIORITIES.get(location, 0)
        distance_to_start = manhattan_distance(start_location, location)
        priority_queue.append((-priority, distance_to_start, location))

    priority_queue.sort(key=lambda x: (x[0], x[1]))

    while priority_queue:
        _, _, goal = priority_queue.pop(0)
        if goal not in visited:
            if algorithm == 'A*':
                path = a_star(start_location, goal)
            else:
                path = dijkstra(start_location, goal)

            if path:
                paths.append(path)
                visited.add(goal)
                start_location = goal
                output.append(1)
            else:
                output.append(0)

    return paths


##########-----parisa-----##########
def animate_paths(paths):
    global canvas
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta", "pink",
              "brown"]  # Define your colors here
    for path in paths:
        color = random.choice(colors)  # Choose a random color for each path
        for node in path:
            row, col = node
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            canvas.update()  # Update the canvas to show the rectangle
            time.sleep(delay / 1000)  # Sleep for the specified delay


##########-----Adrienne-----##########
def display_hospital_map(hospital_map, canvas):
    for row_index, row in enumerate(hospital_map):
        for col_index, cell in enumerate(row):
            x0, y0 = col_index * cell_size, row_index * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            if cell == 1:
                color = "black"
            else:
                color = "white"
                if (row_index, col_index) in PRIORITIES:
                    priority = PRIORITIES[(row_index, col_index)]
                    if priority == 1:
                        color = "blue"
                    elif priority == 2:
                        color = "green"
                    elif priority == 3:
                        color = "yellow"
                    elif priority == 4:
                        color = "orange"
                    elif priority == 5:
                        color = "red"

            canvas.create_rectangle(x0, y0, x1, y1, fill=color)


##########-----parisa-----##########
def open_file(file_path):
    global hospital_map, canvas, previous_paths
    if file_path:
        # Clear the canvas
        canvas.delete("all")
        previous_paths = []  # Reset previous paths

        try:
            with open(file_path, 'r') as file:
                algorithm = file.readline().strip()
                start = file.readline().strip().split(',')
                requests = file.readline().strip().split(', ')
                paths = process_requests([int(x) for x in start], algorithm, requests)
                display_hospital_map(hospital_map, canvas)
                animate_paths(paths)
                if 1 in output:
                    result_message = "SUCCESS"
                else:
                    result_message = "FAILURE"

                result_window = tk.Toplevel(root)
                result_window.title("Result")
                result_label = tk.Label(result_window, text=result_message, font=("Arial", 16))
                result_label.pack(padx=20, pady=20)
        except:
            result_window = tk.Toplevel(root)
            result_window.title("Error")
            result_label = tk.Label(result_window, text="Error in reading file", font=("Arial", 16))
            result_label.pack(padx=20, pady=20)


##########-----parisa&Adrienne-----##########
def main():
    global root, canvas, hospital_map, PRIORITIES
    if len(sys.argv) < 2:
        print("Usage: python findPath.py <file_path>")
        return

    file_path = sys.argv[1]

    image_path = './photo.jpg'
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, (0, 0), fx=1 / 4, fy=1 / 4)
    _, bin_image = cv2.threshold(resized_image, 230, 255, cv2.THRESH_BINARY_INV)
    bin_image[bin_image == 255] = 1
    hospital_map = bin_image.astype(int)

    with open('prio.txt', 'r') as file:
        PRIORITIES = eval(file.read())

    root = tk.Tk()
    root.title("Robot Nurse Path Finder")

    # Canvas for displaying the hospital map and paths
    canvas_width = len(hospital_map[0]) * cell_size
    canvas_height = len(hospital_map) * cell_size
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    display_hospital_map(hospital_map, canvas)
    open_file(file_path)

    root.mainloop()


if __name__ == "__main__":
    main()
