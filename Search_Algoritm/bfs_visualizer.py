"""Visualisasi BFS pada grid, dibuat untuk paket pembelajaran ini."""

from collections import deque
from dataclasses import dataclass
import random
from time import perf_counter
import tkinter as tk
from tkinter import messagebox, ttk

Cell = tuple[int, int]


@dataclass
class SearchStep:
    current: Cell | None
    frontier: tuple[Cell, ...]
    visited: int
    path: tuple[Cell, ...] = ()
    finished: bool = False


def bfs_steps(rows: int, cols: int, walls: set[Cell], start: Cell, goal: Cell):
    """BFS empat arah; setiap langkah menunjukkan satu simpul yang diperiksa."""
    def valid(cell):
        return 0 <= cell[0] < rows and 0 <= cell[1] < cols and cell not in walls

    if not valid(start) or not valid(goal):
        raise ValueError("Titik awal dan tujuan harus berada pada sel yang terbuka.")
    queue = deque([start])
    parents = {start: None}
    visited = 0
    while queue:
        current = queue.popleft()
        visited += 1
        if current == goal:
            path = []
            cell = current
            while cell is not None:
                path.append(cell)
                cell = parents[cell]
            yield SearchStep(current, tuple(queue), visited, tuple(reversed(path)), True)
            return
        row, col = current
        for neighbor in ((row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)):
            if valid(neighbor) and neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
        yield SearchStep(current, tuple(queue), visited)
    yield SearchStep(None, (), visited, finished=True)


class BFSVisualizer:
    COLORS = {
        "empty": "#ffffff", "wall": "#171717", "start": "#22c55e",
        "goal": "#ef4444", "visited": "#fde047", "frontier": "#ddd6fe",
        "path": "#7dd3fc", "current": "#fb923c",
    }

    def __init__(self, root):
        self.root = root
        root.title("Visualisasi Pencarian Jalur — BFS")
        root.geometry("1100x820")
        root.minsize(850, 650)
        self.rows = self.cols = 20
        self.start, self.goal = (0, 0), (19, 19)
        self.walls = set()
        self.visited = set()
        self.frontier = set()
        self.path = set()
        self.current = None
        self.running = False
        self.pending = None
        self.steps = None
        self.elapsed = 0.0
        self.rectangles = {}
        self.cell_size = 1
        self.origin = (0, 0)
        self.mode = tk.StringVar(value="wall")
        self.status = tk.StringVar(value="Atur grid, lalu klik Mulai BFS.")
        self.metrics = tk.StringVar(value="Algoritma: BFS\nGerakan: 4 arah\nBiaya setiap sisi: 1")

        controls = ttk.Frame(root, padding=10)
        controls.pack(fill="x")
        self.row_input = tk.StringVar(value="20")
        self.col_input = tk.StringVar(value="20")
        self.density = tk.StringVar(value="0.2")
        for label, variable, lower, upper, increment in (
            ("Baris", self.row_input, 5, 40, 1),
            ("Kolom", self.col_input, 5, 40, 1),
            ("Kepadatan tembok", self.density, 0, 0.6, 0.05),
        ):
            ttk.Label(controls, text=label).pack(side="left", padx=(0, 5))
            ttk.Spinbox(controls, textvariable=variable, from_=lower, to=upper,
                        increment=increment, width=5).pack(side="left", padx=(0, 12))
        ttk.Button(controls, text="Buat Maze", command=lambda: self.new_grid(True)).pack(side="left", padx=4)
        ttk.Button(controls, text="Kosongkan Grid", command=self.new_grid).pack(side="left", padx=4)

        tools = ttk.LabelFrame(root, text="Klik atau seret pada grid untuk mengedit", padding=10)
        tools.pack(fill="x", padx=10, pady=5)
        for text, value in (("Titik Awal", "start"), ("Tujuan", "goal"),
                            ("Tembok", "wall"), ("Hapus Tembok", "erase")):
            ttk.Radiobutton(tools, text=text, value=value, variable=self.mode).pack(side="left", padx=8)

        actions = ttk.Frame(root, padding=10)
        actions.pack(fill="x")
        self.search_button = ttk.Button(actions, text="Mulai BFS", command=self.search)
        self.search_button.pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Hentikan", command=self.stop).pack(side="left", padx=4)
        ttk.Button(actions, text="Reset Pencarian", command=self.reset).pack(side="left", padx=4)
        ttk.Label(actions, textvariable=self.status).pack(side="left", padx=16)

        content = ttk.Frame(root, padding=10)
        content.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(content, background="#f1f5f9", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.canvas.bind("<Configure>", self.draw_grid)
        self.canvas.bind("<Button-1>", self.edit)
        self.canvas.bind("<B1-Motion>", self.edit)
        sidebar = ttk.LabelFrame(content, text="Metrik dan Warna", padding=15)
        sidebar.pack(side="right", fill="y")
        ttk.Label(sidebar, textvariable=self.metrics, justify="left", width=28).pack(anchor="w", pady=(0, 25))
        for name, label in (("start", "Titik awal"), ("goal", "Tujuan"), ("wall", "Tembok"),
                            ("visited", "Sudah diperiksa"), ("frontier", "Antrean / frontier"),
                            ("current", "Sedang diperiksa"), ("path", "Jalur terpendek")):
            item = ttk.Frame(sidebar)
            item.pack(fill="x", pady=5)
            tk.Label(item, background=self.COLORS[name], width=2, relief="solid", borderwidth=1).pack(side="left", padx=(0, 10))
            ttk.Label(item, text=label).pack(side="left")
        ttk.Label(sidebar, text="BFS menjelajah per tingkat.\nTidak menggunakan heuristik.\n\nMaze acak bisa tidak memiliki\njalur menuju tujuan.", justify="left").pack(anchor="w", pady=25)
        root.protocol("WM_DELETE_WINDOW", self.close)

    def stop(self):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
            self.pending = None
        if self.running:
            self.status.set("Pencarian dihentikan.")
        self.running = False
        self.steps = None
        self.search_button.state(["!disabled"])

    def reset(self):
        self.stop()
        self.visited.clear()
        self.frontier.clear()
        self.path.clear()
        self.current = None
        self.elapsed = 0.0
        self.status.set("Atur grid, lalu klik Mulai BFS.")
        self.update_metrics()
        self.paint()

    def new_grid(self, random_walls=False):
        try:
            rows, cols = int(self.row_input.get()), int(self.col_input.get())
            density = float(self.density.get())
            if not (5 <= rows <= 40 and 5 <= cols <= 40 and 0 <= density <= 0.6):
                raise ValueError
        except ValueError:
            messagebox.showerror("Pengaturan tidak valid", "Baris/kolom harus 5–40 dan kepadatan 0–0.6.")
            return
        self.stop()
        self.rows, self.cols = rows, cols
        self.start, self.goal = (0, 0), (rows - 1, cols - 1)
        self.walls = {(r, c) for r in range(rows) for c in range(cols)
                      if random_walls and random.random() < density
                      and (r, c) not in (self.start, self.goal)}
        self.reset()
        self.draw_grid()

    def draw_grid(self, event=None):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.cell_size = max(1, min((width - 16) / self.cols, (height - 16) / self.rows))
        self.origin = ((width - self.cols * self.cell_size) / 2,
                       (height - self.rows * self.cell_size) / 2)
        self.canvas.delete("all")
        self.rectangles.clear()
        left, top = self.origin
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = left + col * self.cell_size, top + row * self.cell_size
                self.rectangles[row, col] = self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size, outline="#94a3b8")
        self.paint()

    def paint(self):
        for cell, rectangle in self.rectangles.items():
            state = "empty"
            for cells, name in ((self.frontier, "frontier"), (self.visited, "visited"),
                                (self.path, "path"), (self.walls, "wall")):
                if cell in cells:
                    state = name
            if cell == self.current and not self.path:
                state = "current"
            if cell == self.start:
                state = "start"
            elif cell == self.goal:
                state = "goal"
            self.canvas.itemconfigure(rectangle, fill=self.COLORS[state])

    def edit(self, event):
        if self.running:
            return
        left, top = self.origin
        cell = (int((event.y - top) // self.cell_size), int((event.x - left) // self.cell_size))
        if not (0 <= cell[0] < self.rows and 0 <= cell[1] < self.cols):
            return
        mode = self.mode.get()
        if mode == "start" and cell != self.goal:
            self.start = cell
            self.walls.discard(cell)
        elif mode == "goal" and cell != self.start:
            self.goal = cell
            self.walls.discard(cell)
        elif mode == "wall" and cell not in (self.start, self.goal):
            self.walls.add(cell)
        elif mode == "erase":
            self.walls.discard(cell)
        self.reset()

    def update_metrics(self, step=None):
        distance = str(len(step.path) - 1) if step and step.path else "—"
        self.metrics.set(
            f"Algoritma: BFS\nGerakan: 4 arah\nGrid: {self.rows} × {self.cols}\n"
            f"Tembok: {len(self.walls)}\n\nSimpul diperiksa: {len(self.visited)}\n"
            f"Ukuran antrean: {len(self.frontier)}\nJarak jalur (sisi): {distance}\n"
            f"Waktu komputasi: {self.elapsed * 1000:.2f} ms\n\nAnimasi: 20 ms per langkah"
        )

    def search(self):
        self.reset()
        self.steps = bfs_steps(self.rows, self.cols, set(self.walls), self.start, self.goal)
        self.running = True
        self.search_button.state(["disabled"])
        self.status.set("BFS sedang mencari jalur…")
        self.advance()

    def advance(self):
        self.pending = None
        began = perf_counter()
        step = next(self.steps)
        self.elapsed += perf_counter() - began
        self.current = step.current
        if step.current is not None:
            self.visited.add(step.current)
        self.frontier = set(step.frontier)
        self.path = set(step.path)
        self.update_metrics(step)
        self.paint()
        if step.finished:
            self.status.set(f"Jalur ditemukan: {len(step.path) - 1} sisi." if step.path else "Jalur tidak ditemukan.")
            self.running = False
            self.steps = None
            self.search_button.state(["!disabled"])
        else:
            self.pending = self.root.after(20, self.advance)

    def close(self):
        self.stop()
        self.root.destroy()


def launch_gui():
    root = tk.Tk()
    BFSVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
