import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageTk

# Function to convert BGR color to RGB
def bgr_to_rgb(color):
    return color[2], color[1], color[0]

# Function to convert RGB color to BGR
def rgb_to_bgr(color):
    return color[2], color[1], color[0]

# Function to convert RGB color to hexadecimal
def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

# Function to extract major colors from an image
def extract_major_colors(image_path, num_colors=4):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape the image to be a list of pixels
    pixels = img.reshape((-1, 3))

    # Apply KMeans clustering to find major colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers
    major_colors = kmeans.cluster_centers_

    # Convert major colors from RGB to BGR format
    major_colors_bgr = [rgb_to_bgr(tuple(color)) for color in major_colors]

    return major_colors_bgr

# Function to display the color palette
def display_palette(colors):
    palette = np.zeros((100, 240, 3), dtype="uint8")
    hex_labels = []
    for i, color in enumerate(colors):
        color = tuple(map(int, color))
        cv2.rectangle(palette, (i * 60, 0), ((i + 1) * 60, 100), color, -1)
        hex_color = rgb_to_hex(color)
        hex_labels.append(hex_color)

    return palette, hex_labels

# Function to handle the "Generate Palette" button click
def generate_palette():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])

    if file_path:
        major_colors = extract_major_colors(file_path)
        palette_image, hex_labels = display_palette(major_colors)

        # Convert the palette to RGB format for display in Tkinter
        palette_rgb = cv2.cvtColor(palette_image, cv2.COLOR_BGR2RGB)
        palette_img = ImageTk.PhotoImage(Image.fromarray(palette_rgb))

        # Display the image and palette
        image_label.config(image=palette_img, borderwidth=0, highlightthickness=0, relief="flat")
        image_label.image = palette_img
        hex_label.config(text="\n".join(hex_labels), borderwidth=0, border=0, highlightthickness=0, relief="flat")
        save_button.config(state=tk.NORMAL)

# Function to save the color palette
def save_color_palette():
    major_colors = extract_major_colors(file_path)
    palette_image, _ = display_palette(major_colors)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        cv2.imwrite(save_path, palette_image)
        print("Color palette saved as", save_path)

# Create the main window
root = tk.Tk()
root.title("Color Palette Generator")
root.geometry("600x400")  # Set the window size
root.config(bg="#000000", border=0, borderwidth=0, highlightthickness=0, relief="flat")  # Set background color
# Load the background image
#background_image = Image.open("Images/background.png")  # Replace "backgrjjjound.jpg" with the path to your image
#background_photo = ImageTk.PhotoImage(background_image)

# Create a label for the background image
#background_label = tk.Label(root, image=background_photo)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add the background label to the window
#background_label.lower()

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)
button_frame.config(borderwidth=0, border=0, highlightthickness=0, relief="flat")

# Create a button to select an image
generate_button = tk.Button(root, text="Select Image", command=generate_palette, bg="white", fg="black", font=("Helvetica", 12))
generate_button.config(borderwidth=0, border=0, highlightthickness=0, relief="flat")
generate_button.pack(side=tk.BOTTOM, padx=5)

#Create a label to display the color paletste
image_label = tk.Label(root, justify="left", bg="black", fg="black")
image_label.config(borderwidth=0, border=0, highlightthickness=0, relief="flat")
image_label.pack()

# Create a label to display the hexadecimal color numbers
hex_label = tk.Label(root, justify="left", bg="black", fg="white", font=("Helvetica", 12))
hex_label.config(borderwidth=0, border=0, highlightthickness=0, relief="flat")
hex_label.pack()

# Create a button to save the color palettkkke
save_button = tk.Button(root, text="Save Palette", command=generate_palette, bg="white", fg="black", font=("Helvetica", 12))
save_button.config(borderwidth=0, border=0, highlightthickness=0, relief="flat")
save_button.pack(side=tk.BOTTOM, padx=2)



root.mainloop()
