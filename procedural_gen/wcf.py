import random
import copy
from collections import defaultdict, deque, Counter

class Pattern:
    def __init__(self, id):
        self.id = id

class ConstraintGraph:
    def __init__(self):
        # clé = (pattern_id, direction) -> set(des pattern_id compatibles)
        self.rules = defaultdict(set)

    def add(self, a, direction, b):
        self.rules[(a, direction)].add(b)

    def has_direction(self, direction):
        # Est-ce qu’on a au moins une règle pour 'direction' ?
        return any(d == direction for (_, d) in self.rules.keys())

    def compatible(self, a, direction):
        return self.rules.get((a, direction), set())

class Cell:
    def __init__(self, all_ids):
        self.possible = set(all_ids)

    @property
    def entropy(self):
        return len(self.possible)

    @property
    def is_collapsed(self):
        return self.entropy == 1

    def collapse(self, choice):
        self.possible = {choice}

def propagate(grid, graph):
    height, width = len(grid), len(grid[0])
    directions_map = {
        'left':  (-1,  0, 'right'),
        'right': ( 1,  0, 'left'),
        'up':    ( 0, -1, 'down'),
        'down':  ( 0,  1, 'up'),
    }
    active_dirs = [d for d in directions_map if graph.has_direction(d)]

    queue = deque()
    for y in range(height):
        for x in range(width):
            for d in active_dirs:
                dx, dy, _ = directions_map[d]
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    queue.append((x, y, d, nx, ny))

    while queue:
        x, y, d, nx, ny = queue.popleft()
        cell, nbr = grid[y][x], grid[ny][nx]
        before = nbr.possible.copy()

        valid = {
            b for b in nbr.possible
            if any(b in graph.compatible(a, d) for a in cell.possible)
        }

        if not valid:
            return False  # contradiction

        if valid != nbr.possible:
            nbr.possible = valid
            # réenfiler tous les arcs autour de nbr
            for d2 in active_dirs:
                dx2, dy2, _ = directions_map[d2]
                nnx, nny = nx + dx2, ny + dy2
                if 0 <= nnx < width and 0 <= nny < height:
                    queue.append((nx, ny, d2, nnx, nny))

    return True

def solve(grid, graph):
    if not propagate(grid, graph):
        return False

    uncollapsed = [
        (x,y)
        for y,row in enumerate(grid)
        for x,cell in enumerate(row)
        if not cell.is_collapsed
    ]
    if not uncollapsed:
        return True

    x, y = min(
        uncollapsed,
        key=lambda pos: grid[pos[1]][pos[0]].entropy
    )
    cell = grid[y][x]

    options = list(cell.possible)
    random.shuffle(options)
    for choice in options:
        new_grid = copy.deepcopy(grid)
        new_grid[y][x].collapse(choice)
        if solve(new_grid, graph):
            for yy in range(len(grid)):
                for xx in range(len(grid[0])):
                    grid[yy][xx].possible = new_grid[yy][xx].possible
            return True

    return False

class WFC:
    def __init__(self, width, height, patterns, graph):
        self.width = width
        self.height = height
        self.graph = graph
        ids = [p.id for p in patterns]
        self.grid = [[Cell(ids.copy()) for _ in range(width)]
                     for _ in range(height)]

    def run(self):
        return solve(self.grid, self.graph)

    def render(self):
        return [[next(iter(cell.possible)) for cell in row]
                for row in self.grid]

if __name__ == "__main__":
    random.seed()

    patterns = [Pattern(i) for i in range(4)]

    graph = ConstraintGraph()
    for a,b in [(0,1),(1,2),(2,3),(3,2), (0,2), (3,0)]:
        graph.add(b, 'left',  a)

    graph = ConstraintGraph()
    for a,b in [(1,2),(2,1), (1,3),(3,1), (2,3),(3,2), (0,3), (2,0)]:
        graph.add(a, 'down', b)

    wfc = WFC(40, 20, patterns, graph)
    success = wfc.run()
    rendered = wfc.render() if success else wfc.render()

    print("Résultat :", "Succès" if success else "Échec")
    for row in rendered:
        print(" ".join(str(v) for v in row))

