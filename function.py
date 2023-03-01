def find_path(matrix, start, end):
    stack = [start]
    visited = {start: True}
    instructions = {start: None}

    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current != start:
                path.append(instructions[current])
                current = tuple(map(lambda x, y: x - y, current, instructions[current]))
            return list(reversed(path))

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in visited:
                stack.append(neighbor)
                visited[neighbor] = True
                instructions[neighbor] = tuple(map(lambda x, y: x - y, neighbor, current))

    return None

def get_neighbors(matrix, coord):
    rows, cols = len(matrix), len(matrix[0])
    neighbors = []
    for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        row, col = coord[0] + i, coord[1] + j
        if 0 <= row < rows and 0 <= col < cols and matrix[row][col] != '#':
            neighbors.append((row, col))
    return neighbors