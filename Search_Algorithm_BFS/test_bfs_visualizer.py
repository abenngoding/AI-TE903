"""Pemeriksaan pencarian grid terhadap implementasi BFS referensi."""

import random
import unittest

from bfs_visualizer import bfs_steps
from breadth_first_search_shortest_path_2 import bfs_shortest_path


class GridSearchTests(unittest.TestCase):
    def test_shortest_path_on_open_grid(self):
        result = list(bfs_steps(5, 5, set(), (0, 0), (4, 4)))[-1]
        self.assertTrue(result.finished)
        self.assertEqual(len(result.path) - 1, 8)

    def test_unreachable_goal(self):
        result = list(bfs_steps(3, 3, {(1, c) for c in range(3)}, (0, 0), (2, 2)))[-1]
        self.assertTrue(result.finished)
        self.assertEqual(result.path, ())
        self.assertEqual(result.visited, 3)

    def test_start_is_goal(self):
        result = list(bfs_steps(3, 3, set(), (1, 1), (1, 1)))[-1]
        self.assertEqual(result.path, ((1, 1),))
        self.assertEqual(result.visited, 1)

    def test_invalid_endpoints(self):
        for start, goal, walls in (((-1, 0), (2, 2), set()),
                                   ((0, 0), (2, 2), {(2, 2)})):
            with self.assertRaises(ValueError):
                list(bfs_steps(3, 3, walls, start, goal))

    def test_random_mazes_match_reference_bfs(self):
        rng = random.Random(42)
        for _ in range(50):
            start, goal = (0, 0), (4, 4)
            walls = {(r, c) for r in range(5) for c in range(5)
                     if rng.random() < 0.3 and (r, c) not in (start, goal)}
            graph = {}
            for row in range(5):
                for col in range(5):
                    if (row, col) not in walls:
                        graph[row, col] = [cell for cell in (
                            (row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)
                        ) if 0 <= cell[0] < 5 and 0 <= cell[1] < 5 and cell not in walls]
            steps = list(bfs_steps(5, 5, walls, start, goal))
            expected = bfs_shortest_path(graph, start, goal)
            self.assertEqual(list(steps[-1].path), expected)
            examined = [step.current for step in steps if step.current is not None]
            self.assertEqual(len(examined), len(set(examined)))


if __name__ == "__main__":
    unittest.main()
