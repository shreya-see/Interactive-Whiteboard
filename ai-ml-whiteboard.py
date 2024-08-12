import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageTk, ImageFont
import math

class WhiteboardApp:
    def __init__(self, root):
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

    def create_menu(self):
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

    def paint(self, event):
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

    def on_button_press(self, event):
        if self.tool == 'text':
            self.add_text(event)
        else:
            self.start_x, self.start_y = event.x, event.y
            self.current_shape_id = None

    def on_button_release(self, event):
        if self.tool in ['rectangle', 'circle', 'line', 'cube', 'pentagon', 'hexagon', 'triangle', 'star']:
            x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
            x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
            if self.tool == 'rectangle':
                self.draws[self.current_page].rectangle([x0, y0, x1, y1], outline=self.color, width=self.pen_size)
            elif self.tool == 'circle':
                self.draws[self.current_page].ellipse([x0, y0, x1, y1], outline=self.color, width=self.pen_size)
            elif self.tool == 'line':
                self.draws[self.current_page].line([self.start_x, self.start_y, event.x, event.y], fill=self.color, width=self.pen_size)
            elif self.tool == 'cube':
                coords = self.get_cube_coords(x0, y0, x1, y1)
                self.draws[self.current_page].polygon(coords, outline=self.color, width=self.pen_size)
            elif self.tool == 'pentagon':
                self.draws[self.current_page].polygon(self.get_pentagon_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'hexagon':
                self.draws[self.current_page].polygon(self.get_hexagon_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'triangle':
                self.draws[self.current_page].polygon(self.get_triangle_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
            elif self.tool == 'star':
                self.draws[self.current_page].polygon(self.get_star_coords(self.start_x, self.start_y, event.x, event.y), outline=self.color, width=self.pen_size)
        self.start_x, self.start_y = None, None

    def get_cube_coords(self, x0, y0, x1, y1):
        # Calculate the cube coordinates
        width = x1 - x0
        height = y1 - y0

        # Points for the front face
        p1 = (x0, y0)
        p2 = (x1, y0)
        p3 = (x1, y1)
        p4 = (x0, y1)

        # Points for the back face
        p5 = (x0 + width / 2, y0 - height / 2)
        p6 = (x1 + width / 2, y0 - height / 2)
        p7 = (x1 + width / 2, y1 - height / 2)
        p8 = (x0 + width / 2, y1 - height / 2)

        # Return the coordinates for drawing the cube
        return [p1, p2, p6, p7, p3, p4, p8, p5, p1, p5, p6, p2, p3, p7, p8, p4]
    
    def get_pentagon_coords(self, x0, y0, x1, y1):
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        radius = min(abs(x1 - x0), abs(y1 - y0)) / 2
        angle_offset = math.pi / 2  # Start from the top of the pentagon
        coords = []
        for i in range(5):
            angle = angle_offset + i * 2 * math.pi / 5
            x = center_x + radius * math.cos(angle)
            y = center_y - radius * math.sin(angle)
            coords.append((x, y))
        return coords
    
    def get_hexagon_coords(self, x0, y0, x1, y1):
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        radius = min(abs(x1 - x0), abs(y1 - y0)) / 2
        coords = []
        for i in range(6):
            angle = math.radians(60 * i)
            x = center_x + radius * math.cos(angle)
            y = center_y - radius * math.sin(angle)
            coords.append((x, y))
        return coords

    def get_triangle_coords(self, x0, y0, x1, y1):
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        height = abs(y1 - y0) / 2
        base = abs(x1 - x0)
        coords = [
            (x0, y1),
            (x1, y1),
            (center_x, center_y - height)
        ]
        return coords

    def get_star_coords(self, x0, y0, x1, y1):
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        radius = min(abs(x1 - x0), abs(y1 - y0)) / 2
        inner_radius = radius / 2
        angle_offset = math.pi / 2  # Start from the top of the star
        coords = []
        for i in range(5):
            outer_angle = angle_offset + i * 2 * math.pi / 5
            x_outer = center_x + radius * math.cos(outer_angle)
            y_outer = center_y - radius * math.sin(outer_angle)
            coords.append((x_outer, y_outer))
            
            inner_angle = outer_angle + math.pi / 5
            x_inner = center_x + inner_radius * math.cos(inner_angle)
            y_inner = center_y - inner_radius * math.sin(inner_angle)
            coords.append((x_inner, y_inner))
        return coords

    def set_tool(self, tool_name):
        self.tool = tool_name

    def set_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def set_pen_size(self):
        size = simpledialog.askinteger("Pen Size", "Enter pen size:", initialvalue=self.pen_size)
        if size:
            self.pen_size = size

    def set_eraser_size(self):
        size = simpledialog.askinteger("Eraser Size", "Enter eraser size:", initialvalue=self.pen_size)
        if size:
            self.pen_size = size

    def clear_page(self):
        self.pages[self.current_page] = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draws[self.current_page] = ImageDraw.Draw(self.pages[self.current_page])
        self.update_canvas()

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pages[0].save(file_path, save_all=True, append_images=self.pages[1:], resolution=100.0)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            img = Image.open(file_path).resize((self.canvas_width, self.canvas_height))
            self.pages[self.current_page] = img
            self.draws[self.current_page] = ImageDraw.Draw(self.pages[self.current_page])
            self.update_canvas()

    def next_page(self):
        self.current_page += 1
        if self.current_page >= len(self.pages):
            self.pages.append(Image.new("RGB", (self.canvas_width, self.canvas_height), "white"))
            self.draws.append(ImageDraw.Draw(self.pages[self.current_page]))
        self.update_canvas()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self.update_canvas()

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.pages[self.current_page])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def add_text_mode(self):
        self.tool = 'text'

    def set_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.text_options["size"])
        if size:
            self.text_options["size"] = size

    def set_font_style(self):
        style = simpledialog.askstring("Font Style", "Enter font style (normal, bold, italic):", initialvalue=self.text_options["style"])
        if style:
            self.text_options["style"] = style

    def add_text(self, event):
        text = simpledialog.askstring("Input Text", "Enter text:")
        if text:
            font_path = "arial.ttf"  # Use a path to a TrueType font file
            font = ImageFont.truetype(font_path, self.text_options["size"])  # Use ImageFont.truetype instead of tkfont.Font
            self.canvas.create_text(event.x, event.y, text=text, font=(self.text_options["font"], self.text_options["size"], self.text_options["style"]), fill=self.color)
            self.draws[self.current_page].text((event.x, event.y), text, fill=self.color, font=font)
            # Reset tool to pen or another default after adding text
            self.tool = 'pen'


if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root)
    root.mainloop()
