"""Peluncur demo BFS; algoritma asli berasal dari TheAlgorithms/Python.

File peluncur ini ditambahkan untuk paket pembelajaran. Kode algoritma asli
tetap berada di breadth_first_search_shortest_path_2.py.
"""

import argparse

from breadth_first_search_shortest_path_2 import (
    bfs_shortest_path,
    bfs_shortest_path_distance,
    demo_graph,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mencari jalur terpendek pada graf contoh dengan BFS."
    )
    nodes = sorted(demo_graph)
    parser.add_argument("--start", default="G", choices=nodes, help="Simpul awal")
    parser.add_argument("--goal", default="D", choices=nodes, help="Simpul tujuan")
    parser.add_argument("--gui", action="store_true", help="Buka visualisasi BFS pada grid")
    args = parser.parse_args()

    if args.gui:
        from bfs_visualizer import launch_gui

        launch_gui()
        return

    print("Search Algorithm: Breadth-First Search (BFS)")
    print(f"Pencarian: {args.start} -> {args.goal}")
    path = bfs_shortest_path(demo_graph, args.start, args.goal)
    if not path:
        print("Jalur tidak ditemukan.")
        return
    print("Jalur terpendek: " + " -> ".join(path))
    print("Jumlah sisi:", bfs_shortest_path_distance(demo_graph, args.start, args.goal))


if __name__ == "__main__":
    main()
