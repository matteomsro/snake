from queue import Queue
from PIL import Image, ImageOps
import numpy as np


def find_path(matrix, start, end):
    if end == None:
        return None
    
    # Créer une file vide et ajouter le point de départ
    q = [start]
    
    # Créer un dictionnaire pour enregistrer le chemin parcouru
    path = {start: None}
    
    while q:
        current = q.pop(0)
        
        # Si on a atteint le point final, construire la liste de mouvements
        if current == end:
            moves = []
            while current != start:
                parent = path[current]
                diff = tuple(a - b for a, b in zip(current, parent))
                if diff == (-1, 0):
                    moves.append('haut')
                elif diff == (1, 0):
                    moves.append('bas')
                elif diff == (0, -1):
                    moves.append('gauche')
                elif diff == (0, 1):
                    moves.append('droite')
                current = parent
            return moves[::-1]
        
        # Visiter les voisins du point actuel
        for neighbor in get_neighbors(matrix, current):
            if neighbor not in path:
                q.append(neighbor)
                path[neighbor] = current
    
    # Si aucun chemin n'a été trouvé
    return None



def get_neighbors(matrix, point):
    # Récupérer les coordonnées des voisins valides
    neighbors = []
    rows, cols = matrix.shape
    for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        neighbor = (point[0] + move[0], point[1] + move[1])
        if (
            0 <= neighbor[0] < rows and 
            0 <= neighbor[1] < cols and 
            matrix[neighbor[0], neighbor[1]] == 0 
        ):
            neighbors.append(neighbor)
    return neighbors

    return neighbors




if __name__ == "__main__":


    matrix = np.zeros((5, 5), dtype=int)
    matrix[0, :] = -1
    matrix[-1, :] = -1
    matrix[:, 0] = -1
    matrix[:, -1] = -1
    matrix[2, 2] = 1

    # Trouver le chemin entre (1, 1) et (3, 3)
    start = (1, 1)
    end = (3, 3)
    path = find_path(matrix, start, end)

    # Vérifier que le chemin est valide
    print(path)
    assert path == ['droite', 'droite', 'droite', 'bas', 'bas']