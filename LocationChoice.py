import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


##########-----parisa-----##########
# Load the original image
original_image_path = './floorplan1_nolegend.JPG'
original_image = cv2.imread(original_image_path)

# Load and process the image
image_path = './photo.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
resized_image = cv2.resize(image, (0, 0), fx=1 / 4, fy=1 / 4)
_, bin_image = cv2.threshold(resized_image, 230, 255, cv2.THRESH_BINARY_INV)
bin_image[bin_image == 255] = 1

bin_image_int = bin_image.astype(int)
np.savetxt('bin_image.txt', bin_image_int, fmt='%d')

# Assuming bin_image is already defined
bin_image_shape = bin_image.shape

# Define the size of each cell in the grid
cell_size = 3

# List to store selected cells' positions
selected_cells = []

# Variable to store the currently selected cell
current_cell = None


##########-----Adrienne-----##########
# Function to handle cell selection
def cell_clicked(event):
    global current_cell
    # Get the row and column indices of the clicked cell
    row = event.y // cell_size
    col = event.x // cell_size

    # Update the current_cell
    current_cell = (row, col)

    # If the cell is not already selected, add it to the list
    if (row, col) not in selected_cells:
        selected_cells.append((row, col))
        # Highlight the selected cell
        canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size,
                                fill='red')
    else:
        # If the cell is already selected, deselect it
        selected_cells.remove((row, col))
        # Remove the highlighting
        canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size,
                                fill='white')


##########-----parisa-----##########
# Function to handle keyboard input
def handle_keyboard(event):
    global current_cell
    if current_cell is None:
        return

    # Get the row and column indices of the current cell
    row, col = current_cell

    # Check which key was pressed
    if event.keysym == 'Right':
        col += 1
    elif event.keysym == 'Left':
        col -= 1
    elif event.keysym == 'Down':
        row += 1
    elif event.keysym == 'Up':
        row -= 1

    # Update the current cell
    current_cell = (row, col)

    # If the new cell is not already selected, add it to the list
    if (row, col) not in selected_cells:
        selected_cells.append((row, col))
        # Highlight the selected cell
        canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size,
                                fill='red')


# Function to print selected cells
def print_selected_cells():
    for cell in selected_cells:
        print(cell)



##########-----parisa&Adrienne-----##########
# Create a Tkinter application
root = tk.Tk()
root.title("Binary Image Grid")

# Create a canvas to draw the grid
canvas = tk.Canvas(root, width=bin_image_shape[1] * cell_size, height=bin_image_shape[0] * cell_size)
canvas.pack()

# Draw rectangles based on the binary image
for i in range(bin_image_shape[0]):
    for j in range(bin_image_shape[1]):
        color = 'black' if bin_image[i, j] == 1 else 'white'
        canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)

# Bind mouse click event to cell_clicked function
canvas.bind("<Button-1>", cell_clicked)

# Bind keyboard event to handle_keyboard function
root.bind("<Key>", handle_keyboard)

# Create a button to print selected cells
print_button = tk.Button(root, text="Print Selected Cells", command=print_selected_cells)
print_button.pack()

# Run the Tkinter event loop
root.mainloop()

# print(bin_image.shape)
# Display the images
# plt.figure(figsize=(15, 5))

# # Original Image
# plt.subplot(1, 2, 1)
# plt.title('Original Image')
# plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

# # Resized Image
# plt.subplot(1, 2, 2)
# plt.title('Binarized Image')
# plt.imshow(bin_image, cmap='gray')

# plt.show()