This code provides a basic whiteboard application with functionalities to draw various shapes, use different tools, and manage multiple pages. You can build upon this foundation to add more features and enhancements as needed.

1. import tkinter as tk
A standard Python library for creating graphical user interfaces (GUIs).

2. from tkinter import simpledialog, filedialog, colorchooser
Modules for creating dialog boxes.

3. from tkinter import font as tkfont
Module for working with fonts.

4. from PIL import Image, ImageDraw, ImageTk, ImageFont
Used for creating and editing images.

5. import math
A standard Python library for mathematical functions.

6. class WhiteboardApp:
Defines a class named WhiteboardApp which will contain all the functionality of the whiteboard application.

7.     def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")
        self.canvas_width, self.canvas_height = 1600, 1200

        self.pages = [Image.new("RGB", (self.canvas_width, self.canvas_height), "white")]
        self.draws = [ImageDraw.Draw(self.pages[0])]
        self.current_page = 0

        self.canvas = tk.Canvas(root, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x, self.start_y = None, None
        self.current_shape_id = None
        self.color = 'black'
        self.pen_size = 2
        self.tool = 'pen'
        self.text_options = {
            "font": "Arial",
            "size": 20,
            "style": "normal"
        }

        self.create_menu()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.update_canvas() 

7.1 __init__ function: Initializes the whiteboard application.
7.2 self.root: Stores the root window.
7.3 self.root.title("Whiteboard"): Sets the window title to "Whiteboard".
7.4 self.canvas_width, self.canvas_height: Sets the dimensions of the canvas.
7.5 self.pages: A list to store image pages. The first page is created as a white image.
7.6 self.draws: A list to store drawing contexts for each page.
7.7 self.current_page: Tracks the currently active page.
7.8 self.canvas: Creates a canvas widget with a white background.
7.9 self.start_x, self.start_y: Initialize coordinates for drawing shapes.
7.10 self.current_shape_id: ID of the current shape being drawn.
7.11 self.color: Sets the initial pen color to black.
7.12 self.pen_size: Sets the initial pen size.
7.13 self.tool: Sets the initial tool to pen.
7.14 self.text_options: Sets default text options (font, size, style).
7.15 self.create_menu(): Calls a method to create the menu.
7.16 self.canvas.bind: Binds mouse events to methods for drawing.
7.17 self.update_canvas(): Updates the canvas to show the current page.

8.     def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_as_pdf)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        page_menu = tk.Menu(menu)
        menu.add_cascade(label="Page", menu=page_menu)
        page_menu.add_command(label="Next Page", command=self.next_page)
        page_menu.add_command(label="Previous Page", command=self.previous_page)

        shapes_menu = tk.Menu(menu)
        menu.add_cascade(label="Shapes", menu=shapes_menu)
        shapes_menu.add_command(label="Rectangle", command=lambda: self.set_tool('rectangle'))
        shapes_menu.add_command(label="Circle", command=lambda: self.set_tool('circle'))
        shapes_menu.add_command(label="Line", command=lambda: self.set_tool('line'))
        shapes_menu.add_command(label="Cube", command=lambda: self.set_tool('cube'))
        shapes_menu.add_command(label="Pentagon", command=lambda: self.set_tool('pentagon'))
        shapes_menu.add_command(label="Hexagon", command=lambda: self.set_tool('hexagon'))
        shapes_menu.add_command(label="Triangle", command=lambda: self.set_tool('triangle'))
        shapes_menu.add_command(label="Star", command=lambda: self.set_tool('star'))

        text_menu = tk.Menu(menu)
        menu.add_cascade(label="Text", menu=text_menu)
        text_menu.add_command(label="Add Text", command=self.add_text_mode)
        text_menu.add_command(label="Set Font Size", command=self.set_font_size)
        text_menu.add_command(label="Set Font Style", command=self.set_font_style)

        pen_menu = tk.Menu(menu)
        menu.add_cascade(label="Pen", menu=pen_menu)
        pen_menu.add_command(label="Pen", command=lambda: self.set_tool('pen'))
        pen_menu.add_command(label="Set Color", command=self.set_color)
        pen_menu.add_command(label="Set Pen Size", command=self.set_pen_size)
        pen_menu.add_command(label="Clear", command=self.clear_page)
        pen_menu.add_separator()
        pen_menu.add_command(label="Eraser", command=lambda: self.set_tool('eraser'))
        pen_menu.add_command(label="Set Eraser Size", command=self.set_eraser_size)

8.1 create_menu: Defines the menu structure for the application.
8.2 menu: Creates the main menu.
8.3 file_menu: Adds a "File" menu with options to save, open, and exit.
8.4 page_menu: Adds a "Page" menu with options to navigate pages.
8.5 shapes_menu: Adds a "Shapes" menu with options to draw different shapes.
8.6 text_menu: Adds a "Text" menu with options to add text and set font properties.
8.7 pen_menu: Adds a "Pen" menu with options to use the pen, set its color and size, clear the page, and use the eraser.

9.     def paint(self, event):
        if self.tool == 'pen':
            if self.start_x and self.start_y:
                self.canvas.create_line((self.start_x, self.start_y, event.x, event.y),
                                        fill=self.color, width=self.pen_size)
                self.draws[self.current_page].line([(self.start_x, self.start_y), (event.x, event.y)],
                                                   fill=self.color, width=self.pen_size)
            self.start_x, self.start_y = event.x, event.y
        elif self.tool == 'eraser':
            if self.start_x and self.start_y:
                self.canvas.create_line((self.start_x, self.start_y, event.x, event.y),
                                        fill='white', width=self.pen_size)
                self.draws[self.current_page].line([(self.start_x, self.start_y), (event.x, event.y)],
                                                   fill='white', width=self.pen_size)
            self.start_x, self.start_y = event.x, event.y
        elif self.tool in ['rectangle', 'circle', 'line', 'cube', 'pentagon', 'hexagon', 'triangle', 'star']:
            if self.current_shape_id:
                self.canvas.delete(self.current_shape_id)
            if self.tool == 'rectangle':
                self.current_shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_size)
            elif self.tool == 'circle':
                self.current_shape_id = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_size)
            elif self.tool == 'line':
                self.current_shape_id = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.pen_size)
            elif self.tool == 'cube':
                coords = self.get_cube_coords(self.start_x, self.start_y, event.x, event.y)
                self.current_shape_id = self.canvas.create_polygon(coords, outline=self.color, width=self.pen_size, fill='')
            elif self.tool == 'pentagon':
                self.current_shape_id = self.canvas.create_polygon(self.get_pentagon_coords(self.start_x, self.start_y, event.x, event.y),
                                                                   outline=self.color, width=self.pen_size, fill='')
            elif self.tool == 'hexagon':
                self.current_shape_id = self.canvas.create_polygon(self.get_hexagon_coords(self.start_x, self.start_y, event.x, event.y),
                                                                   outline=self.color, width=self.pen_size, fill='')
            elif self.tool == 'triangle':
                self.current_shape_id = self.canvas.create_polygon(self.get_triangle_coords(self.start_x, self.start_y, event.x, event.y),
                                                                   outline=self.color, width=self.pen_size, fill='')
            elif self.tool == 'star':
                self.current_shape_id = self.canvas.create_polygon(self.get_star_coords(self.start_x, self.start_y, event.x, event.y),
                                                                   outline=self.color, width=self.pen_size, fill='')

9.1 paint: Handles drawing based on the selected tool.
9.2 pen: Draws freehand lines.
9.3 eraser: Erases by drawing white lines.
9.4 shapes: Draws shapes based on the current tool. Deletes the previous shape if a new one is being drawn.
9.5 self.canvas.create_line: Draws a line on the canvas.
9.6 self.canvas.create_rectangle, self.canvas.create_oval, self.canvas.create_polygon: Draw shapes on the canvas.
9.7 self.draws[self.current_page].line: Draws lines on the image.

10.     def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_button_release(self, event):
        if self.tool in ['rectangle', 'circle', 'line', 'cube', 'pentagon', 'hexagon', 'triangle', 'star']:
            if self.tool == 'rectangle':
                self.draws[self.current_page].rectangle([self.start_x, self.start_y, event.x, event.y], outline=self.color, width=self.pen_size)
            elif self.tool == 'circle':
                self.draws[self.current_page].ellipse([self.start_x, self.start_y, event.x, event.y], outline=self.color, width=self.pen_size)
            elif self.tool == 'line':
                self.draws[self.current_page].line([self.start_x, self.start_y, event.x, event.y], fill=self.color, width=self.pen_size)
            elif self.tool == 'cube':
                coords = self.get_cube_coords(self.start_x, self.start_y, event.x, event.y)
                self.draws[self.current_page].polygon(coords, outline=self.color, width=self.pen_size)
            elif self.tool == 'pentagon':
                self.draws[self.current_page].polygon(self.get_pentagon_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'hexagon':
                self.draws[self.current_page].polygon(self.get_hexagon_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'triangle':
                self.draws[self.current_page].polygon(self.get_triangle_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'star':
                self.draws[self.current_page].polygon(self.get_star_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
        self.current_shape_id = None

10.1 on_button_press: Stores the starting coordinates for drawing.
10.2 on_button_release: Finalizes the shape and draws it on the image.

11.     def get_cube_coords(self, x1, y1, x2, y2):
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        if width > height:
            width = height
        else:
            height = width

        x3, y3 = x1, y1 + height
        x4, y4 = x1 + width, y1 + height
        x5, y5 = x1 + width / 2, y1 + height / 2
        x6, y6 = x1 + width / 2, y1 + height + height / 2
        x7, y7 = x1 + width + width / 2, y1 + height / 2
        x8, y8 = x1 + width + width / 2, y1 + height + height / 2

        return [(x1, y1), (x2, y2), (x4, y4), (x3, y3), (x1, y1),
                (x5, y5), (x6, y6), (x8, y8), (x7, y7), (x5, y5),
                (x7, y7), (x2, y2), (x6, y6), (x4, y4), (x8, y8)]

11.1 get_cube_coords: Calculates the coordinates for drawing a cube.

12. if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root)
    root.mainloop()

12.1 if name == "main": Ensures the code runs only if the file is executed directly.
12.2 tk.Tk(): Creates the main window.
12.3 WhiteboardApp(root): Creates an instance of the WhiteboardApp class.
12.4 root.mainloop(): Starts the Tkinter event loop.
