from queue import Queue

def find_path(matrix, start, end):
    # Créer une file vide et ajouter le point de départ
    q = Queue()
    q.put(start)

    # Créer un dictionnaire pour enregistrer le chemin parcouru
    path = {start: None}

    while not q.empty():
        current = q.get()

        # Si on a atteint le point final, construire la liste de mouvements
        if current == end:
            moves = []
            while current != start:
                parent = path[current]
                if parent[0] < current[0]:
                    moves.append('bas')
                elif parent[0] > current[0]:
                    moves.append('haut')
                elif parent[1] < current[1]:
                    moves.append('droite')
                elif parent[1] > current[1]:
                    moves.append('gauche')
                current = parent
            return moves[::-1]

        # Visiter les voisins du point actuel
        for neighbor in get_neighbors(matrix, current):
            if neighbor not in path:
                q.put(neighbor)
                path[neighbor] = current

    # Si on ne peut pas trouver de chemin, retourner None
    return None

def get_neighbors(matrix, point):
    # Récupérer les coordonnées des voisins valides
    neighbors = []
    rows, cols = len(matrix), len(matrix[0])
    row, col = point
    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < rows and 0 <= c < cols and matrix[r][c] != 'X':
            neighbors.append((r, c))
    return neighbors
