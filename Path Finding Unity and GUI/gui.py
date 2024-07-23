import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import os
import heapq

class Point:
    def __init__(self, x, y, name, id):
        self.x = x
        self.y = y
        self.name = name
        self.id = id
        self.original_x = x
        self.original_y = y

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

class Link:
    def __init__(self, point1, point2, cost):
        self.point1 = point1
        self.point2 = point2
        self.cost = cost

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Indoor Navigation Annotator")
        self.points = []
        self.links = []
        self.point_id_counter = 1
        self.image = None
        self.tk_image = None
        self.current_mode = 'add_point'  # Modes: add_point, link_points, delete
        self.selected_point = None
        self.previous_searched_node = None
        self.zoom_factor = 1.0
        self.current_path = None

        # Create the canvas for image display
        self.canvas = tk.Canvas(root, cursor="cross", bg='white')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Create the menu
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Image", command=self.open_image)
        self.file_menu.add_command(label="Save Points", command=self.save_points)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.mode_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Mode", menu=self.mode_menu)
        self.mode_menu.add_command(label="Add Point", command=self.set_add_point_mode)
        self.mode_menu.add_command(label="Link Points", command=self.set_link_points_mode)
        self.mode_menu.add_command(label="Delete", command=self.set_delete_mode)

        self.path_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Path", menu=self.path_menu)
        self.path_menu.add_command(label="Find Path", command=self.find_path)

        self.search_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Search", menu=self.search_menu)
        self.search_menu.add_command(label="Search Point", command=self.search_point)

        # Bind the left mouse button click event to the handle_click method
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<B1-Motion>", self.pan)

        self.last_x, self.last_y = None, None

    def open_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.image = Image.open(file_path)
                # Resize the image
                self.fit_image_to_screen()
                self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
                self.points.clear()
                self.links.clear()
                self.point_id_counter = 1
                self.current_path = None
                self.root.title(f"Indoor Navigation Annotator - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    def fit_image_to_screen(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width, image_height = self.image.size

        scale = min(canvas_width / image_width, canvas_height / image_height)
        new_size = (int(image_width * scale), int(image_height * scale))

        self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)

    def handle_click(self, event):
        if self.current_mode == 'add_point':
            self.add_point(event)
        elif self.current_mode == 'link_points':
            self.link_points(event)
        elif self.current_mode == 'delete':
            self.delete_item(event)

    def add_point(self, event):
        if self.image:
            name = simpledialog.askstring("Input", "Enter name for the point:")
            if name:
                adjusted_x = event.x / self.zoom_factor
                adjusted_y = event.y / self.zoom_factor
                point = Point(adjusted_x, adjusted_y, name, self.point_id_counter)
                self.points.append(point)
                self.point_id_counter += 1
                self._draw_point(point)
        else:
            messagebox.showwarning("Warning", "Please open an image first.")

    def link_points(self, event):
        if self.image:
            for point in self.points:
                if abs(point.x * self.zoom_factor - event.x) < 5 and abs(point.y * self.zoom_factor - event.y) < 5:
                    if self.selected_point is None:
                        self.selected_point = point
                        messagebox.showinfo("Info", f"Selected point {point.name}. Now click on another point to link.")
                    else:
                        if self.selected_point != point:
                            cost = simpledialog.askfloat("Input", "Enter cost for the link:")
                            if cost is not None:
                                link = Link(self.selected_point, point, cost)
                                self.links.append(link)
                                self.links.append(Link(point, self.selected_point, cost))  # Add bidirectional link
                                self._draw_link(link)
                            self.selected_point = None
                        else:
                            messagebox.showwarning("Warning", "Cannot link a point to itself.")
                    break
        else:
            messagebox.showwarning("Warning", "Please open an image first.")

    def delete_item(self, event):
        if self.image:
            for point in self.points:
                if abs(point.x * self.zoom_factor - event.x) < 5 and abs(point.y * self.zoom_factor - event.y) < 5:
                    self.points.remove(point)
                    self.links = [link for link in self.links if link.point1 != point and link.point2 != point]
                    self.current_path = None
                    self.redraw_canvas()
                    return

            for link in self.links:
                if self.is_near_line(link, event.x / self.zoom_factor, event.y / self.zoom_factor):
                    self.links.remove(link)
                    self.current_path = None
                    self.redraw_canvas()
                    return

            messagebox.showwarning("Warning", "No point or link found to delete.")
        else:
            messagebox.showwarning("Warning", "Please open an image first.")

    def is_near_line(self, link, x, y):
        # Check if a point (x, y) is near the line segment defined by link
        dist = abs((link.point2.y - link.point1.y) * x - (link.point2.x - link.point1.x) * y + link.point2.x * link.point1.y - link.point2.y * link.point1.x) / \
               ((link.point2.y - link.point1.y)**2 + (link.point2.x - link.point1.x)**2)**0.5
        return dist < 5

    def set_add_point_mode(self):
        self.current_mode = 'add_point'
        self.selected_point = None
        messagebox.showinfo("Mode", "Add Point mode activated.")

    def set_link_points_mode(self):
        if not self.points:
            messagebox.showwarning("Warning", "No points available to link.")
            return
        self.current_mode = 'link_points'
        self.selected_point = None
        messagebox.showinfo("Mode", "Link Points mode activated. Select a point to start linking.")

    def set_delete_mode(self):
        self.current_mode = 'delete'
        self.selected_point = None
        messagebox.showinfo("Mode", "Delete mode activated. Click on a point or link to delete.")

    def _draw_point(self, point):
        radius = 5
        self.canvas.create_oval(
            point.x * self.zoom_factor - radius, point.y * self.zoom_factor - radius, 
            point.x * self.zoom_factor + radius, point.y * self.zoom_factor + radius, 
            fill="red"
        )
        self.canvas.create_text(
            point.x * self.zoom_factor, point.y * self.zoom_factor, 
            text=f"{point.name}", 
            anchor=tk.NW, fill="blue", font=("Helvetica", 9, "bold")
        )

    def _draw_link(self, link):
        self.canvas.create_line(
            link.point1.x * self.zoom_factor, link.point1.y * self.zoom_factor, 
            link.point2.x * self.zoom_factor, link.point2.y * self.zoom_factor, 
            fill="green"
        )
        mid_x = (link.point1.x + link.point2.x) * self.zoom_factor / 2
        mid_y = (link.point1.y + link.point2.y) * self.zoom_factor / 2
        self.canvas.create_text(
            mid_x, mid_y, 
            text=f"{link.cost}", 
            anchor=tk.NW, fill="purple", font=("Helvetica", 9, "bold")
        )

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        for point in self.points:
            self._draw_point(point)
        for link in self.links:
            self._draw_link(link)
        if self.current_path:
            self.highlight_path(self.current_path)

    def save_points(self):
        if not self.points:
            messagebox.showwarning("Warning", "No points to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for point in self.points:
                        f.write(f"{point.id}:{point.name}:{point.x:.2f}:{point.y:.2f}\n")
                    f.write('%\n')
                    for link in self.links:
                        f.write(f"{link.point1.id}:{link.point2.id}:{link.cost}\n")
                messagebox.showinfo("Info", f"Points and links saved successfully to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save points: {e}")

    def find_path(self):
        if not self.points or not self.links:
            messagebox.showwarning("Warning", "Please add points and links before finding a path.")
            return

        source_id = simpledialog.askinteger("Input", "Enter ID of source point:")
        dest_id = simpledialog.askinteger("Input", "Enter ID of destination point:")

        source_point = None
        dest_point = None

        for point in self.points:
            if point.id == source_id:
                source_point = point
            if point.id == dest_id:
                dest_point = point

        if not source_point or not dest_point:
            messagebox.showerror("Error", "Invalid source or destination point ID.")
            return

        # Run Dijkstra's algorithm to find the shortest path
        path_cost, shortest_path = self.dijkstra(source_point, dest_point)
        if path_cost is not None:
            self.current_path = shortest_path
            self.highlight_path(shortest_path)
            messagebox.showinfo("Info", f"Shortest Path Cost: {path_cost}")

    def dijkstra(self, source, destination):
        # Initialize distances and previous nodes
        distances = {point: float('inf') for point in self.points}
        previous = {point: None for point in self.points}
        distances[source] = 0
        visited = set()

        # Use heapq (priority queue) for efficient processing
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_point = heapq.heappop(priority_queue)

            if current_point == destination:
                break

            if current_point in visited:
                continue

            visited.add(current_point)

            for link in self.links:
                if link.point1 == current_point:
                    neighbor = link.point2
                    new_distance = current_distance + link.cost
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_point
                        heapq.heappush(priority_queue, (new_distance, neighbor))

        if distances[destination] == float('inf'):
            messagebox.showerror("Error", "No path found between the selected points.")
            return None, None

        # Construct the shortest path
        shortest_path = []
        current = destination
        while current is not None:
            shortest_path.append(current)
            current = previous[current]
        shortest_path.reverse()

        return distances[destination], shortest_path

    def highlight_path(self, path):
        for i in range(len(path) - 1):
            point1 = path[i]
            point2 = path[i + 1]
            for link in self.links:
                if (link.point1 == point1 and link.point2 == point2) or (link.point1 == point2 and link.point2 == point1):
                    self.canvas.create_line(
                        link.point1.x * self.zoom_factor, link.point1.y * self.zoom_factor, 
                        link.point2.x * self.zoom_factor, link.point2.y * self.zoom_factor, 
                        fill="red", width=3, dash=(4, 4)  # Using a dashed line with thickness 3
                    )

        # Add markers or arrows at each point along the path
        for point in path:
            self.canvas.create_oval(
                point.x * self.zoom_factor - 3, point.y * self.zoom_factor - 3, 
                point.x * self.zoom_factor + 3, point.y * self.zoom_factor + 3, 
                fill="red", outline="red"
            )  # You can change the marker style as per your preference

    def zoom(self, event):
        if self.image:
            scale = 1.0
            if event.delta > 0:
                scale = 1.1
                self.zoom_factor *= scale
            elif event.delta < 0:
                scale = 0.9
                self.zoom_factor *= scale

            new_width = int(self.image.width * scale)
            new_height = int(self.image.height * scale)
            self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.redraw_canvas()

    def pan(self, event):
        if self.last_x and self.last_y:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.canvas.move(tk.ALL, dx, dy)
        self.last_x, self.last_y = event.x, event.y

    def search_point(self):
        if not self.points:
            messagebox.showwarning("Warning", "No points to search.")
            return

        search_name = simpledialog.askstring("Search Point", "Enter name of the point:")
        if search_name:
            if self.previous_searched_node:
                self.redraw_canvas()
            for point in self.points:
                if point.name == search_name:
                    self.canvas.create_oval(
                        point.x * self.zoom_factor - 10, point.y * self.zoom_factor - 10,
                        point.x * self.zoom_factor + 10, point.y * self.zoom_factor + 10,
                        outline="yellow", width=2
                    )
                    self.previous_searched_node = point
                    messagebox.showinfo("Search Result", f"Point found: {point.name} at ({point.x}, {point.y})")
                    return
            messagebox.showwarning("Search Result", "Point not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()