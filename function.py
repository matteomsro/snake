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
        for neighbor in get_neighbors(matrix, current, end):
            if neighbor not in path:
                q.append(neighbor)
                path[neighbor] = current
    
    # Si aucun chemin n'a été trouvé
    return None



def get_neighbors(matrix, point, end):
    # Récupérer les coordonnées des voisins valides
    neighbors = []
    rows, cols = matrix.shape
    row, col = point
    if (row - 1 >= 0) and (col<cols) and (matrix[row - 1, col] != 1):
        neighbors.append((row - 1, col))
    if (row + 1 < rows) and (col<cols) and (matrix[row + 1, col] != 1):
        neighbors.append((row + 1, col))
    if (col - 1 >= 0) and (row<rows) and (matrix[row, col - 1] != 1):
        neighbors.append((row, col - 1))
    if (col + 1 < cols) and (row<rows) and (matrix[row, col + 1] != 1):
        neighbors.append((row, col + 1))

    return neighbors




