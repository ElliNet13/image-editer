import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import numpy as np
import json

class ImageEditorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Editor")

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.color_map = {
            0: (0, 0, 0),    # Black
            1: (255, 255, 255)    # White
        }

        self.image_array = np.zeros((10, 10), dtype=int)
        self.current_color = 0

        self.create_widgets()
        self.draw_image()  # Draw image on initialization

    def create_widgets(self):
        self.color_label = tk.Label(self.master, text="Color:")
        self.color_label.pack()

        self.color_dropdown_var = tk.StringVar(self.master)
        self.color_dropdown = tk.OptionMenu(self.master, self.color_dropdown_var, *self.color_map.keys(), command=self.update_color)
        self.color_dropdown.pack()

        self.add_color_button = tk.Button(self.master, text="Add Color", command=self.add_color)
        self.add_color_button.pack()

        self.delete_color_button = tk.Button(self.master, text="Delete Color", command=self.delete_color)
        self.delete_color_button.pack()

        self.canvas.bind("<Button-1>", self.paint)

        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.save_json_button = tk.Button(self.master, text="Save JSON", command=self.save_json)
        self.save_json_button.pack()

        self.load_json_button = tk.Button(self.master, text="Load JSON", command=self.load_json)
        self.load_json_button.pack()

    def add_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            color_code = max(self.color_map.keys()) + 1
            self.color_map[color_code] = tuple(int(x) for x in color)
            self.update_color_dropdown()

    def delete_color(self):
        if len(self.color_map) > 2:
            color_code = max(self.color_map.keys())
            del self.color_map[color_code]
            self.update_color_dropdown()
        else:
            print("Cannot delete default colors.")

    def update_color_dropdown(self):
        menu = self.color_dropdown['menu']
        menu.delete(0, 'end')
        for color_code in self.color_map.keys():
            menu.add_command(label=f"Color {color_code}", command=lambda color_code=color_code: self.update_color(color_code))

    def update_color(self, color_code):
        self.current_color = int(color_code)

    def paint(self, event):
        x, y = event.x, event.y
        x /= 40
        y /= 40
        x = int(x)
        y = int(y)
        self.image_array[y, x] = self.current_color
        self.draw_image()

    def draw_image(self):
        self.canvas.delete("all")
        for y in range(self.image_array.shape[0]):
            for x in range(self.image_array.shape[1]):
                color_code = self.image_array[y][x]
                color = "#{:02x}{:02x}{:02x}".format(*self.color_map[color_code])
                self.canvas.create_rectangle(x * 40, y * 40, (x + 1) * 40, (y + 1) * 40, fill=color)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], initialfile="image.png")
        if file_path:
            image = np.zeros((self.image_array.shape[0], self.image_array.shape[1], 3), dtype=np.uint8)
            for y in range(self.image_array.shape[0]):
                for x in range(self.image_array.shape[1]):
                    image[y, x] = self.color_map[self.image_array[y, x]]
            image = Image.fromarray(image)
            image.save(file_path)

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="image.json")
        if file_path:
            data = {
                "color_map": {int(k): v for k, v in self.color_map.items()},
                "number_array": self.image_array.tolist()
            }
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            self.color_map = {int(k): tuple(v) for k, v in data["color_map"].items()}
            self.image_array = np.array(data["number_array"])
            self.update_color_dropdown()
            self.draw_image()

root = tk.Tk()
app = ImageEditorGUI(root)
root.mainloop()