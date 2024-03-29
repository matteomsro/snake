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
    x, y = point
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < matrix.shape[0] and 0 <= new_y < matrix.shape[1]
                and matrix[new_x, new_y] != -1 and ((dx == 0) or matrix[x+dx, y] != -1) and ((dy == 0) or matrix[x, y+dy] != -1)):
            neighbors.append((new_x, new_y))
    return neighbors


    return neighbors




