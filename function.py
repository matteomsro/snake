from queue import Queue
from PIL import Image, ImageOps
import numpy as np

def surround_matrix(matrix):
    m, n = matrix.shape
    surrounded = np.zeros((m + 2, n + 2), dtype=int)
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 'X':
                surrounded[i + 1][j + 1] = 1
    return surrounded

def find_path(matrix, start, end):
    if end==None:
        return None
    moves=[]
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
        for neighbor in get_neighbors(matrix, current,end):
            if neighbor not in path:
                q.put(neighbor)
                path[neighbor] = current

def get_neighbors(matrix, point, end):
    # Récupérer les coordonnées des voisins valides
    neighbors = []
    rows, cols = matrix.shape
    row, col = point
    if (row - 1 >= 0) and (matrix[row - 1, col] != 1):
        neighbors.append((row - 1, col))
    if (row + 1 < rows) and (matrix[row + 1, col] != 1):
        neighbors.append((row + 1, col))
    if (col - 1 >= 0) and (matrix[row, col - 1] != 1):
        neighbors.append((row, col - 1))
    if (col + 1 < cols) and (matrix[row, col + 1] != 1):
        neighbors.append((row, col + 1))

    # Ajouter la case adjacente au mur si c'est la seule option pour atteindre la pomme
    if (end in neighbors) and (len(neighbors) == 1):
        wall_neighbors = []
        if (row - 1 >= 0) and (matrix[row - 1, col] == 1):
            wall_neighbors.append((row - 1, col))
        if (row + 1 < rows) and (matrix[row + 1, col] == 1):
            wall_neighbors.append((row + 1, col))
        if (col - 1 >= 0) and (matrix[row, col - 1] == 1):
            wall_neighbors.append((row, col - 1))
        if (col + 1 < cols) and (matrix[row, col + 1] == 1):
            wall_neighbors.append((row, col + 1))
        neighbors.extend(wall_neighbors)

    return neighbors


def find_shortest_path(image_path):
    # Ouvrir l'image en niveau de gris et inverser les couleurs
    image = ImageOps.invert(Image.open(image_path).convert('L'))
    # Convertir l'image en un tableau numpy
    matrix = np.array(image)
    # Ajouter une bordure de murs autour de la matrice
    surrounded = surround_matrix(matrix)
    # Trouver les points de départ et d'arrivée
    start = np.argwhere(matrix == 0)[0]
    end = np.argwhere(matrix == 255)[-1]
    # Trouver le chemin le plus court
    path = find_path(surrounded, tuple(start + 1), tuple(end + 1))
    
    # Si le chemin est nul, il y a une erreur, renvoyer une liste vide
    if path is None:
        return []
    
    # Si la longueur du chemin est inférieure à 2, retourner le chemin tel quel
    if len(path) < 2:
        return path
    
    # Vérifier si le serpent se dirige vers le mur
    if path[0] == 'bas' and matrix[start[0]+1][start[1]] == 1:
        # Si le serpent va vers le bas et rencontre un mur, essayer de tourner à gauche ou à droite
        if matrix[start[0]][start[1]-1] != 1:
            return ['gauche'] + path
        elif matrix[start[0]][start[1]+1] != 1:
            return ['droite'] + path
    elif path[0] == 'haut' and matrix[start[0]-1][start[1]] == 1:
        # Si le serpent va vers le haut et rencontre un mur, essayer de tourner à gauche ou à droite
        if matrix[start[0]][start[1]-1] != 1:
            return ['gauche'] + path
        elif matrix[start[0]][start[1]+1] != 1:
            return ['droite'] + path
    elif path[0] == 'droite' and matrix[start[0]][start[1]+1] == 1:
        # Si le serpent va vers la droite et rencontre un mur, essayer de tourner en haut ou en bas
        if matrix[start[0]-1][start[1]] != 1:
            return ['haut'] + path
        elif matrix[start[0]+1][start[1]] != 1:
            return ['bas'] + path
    elif path[0] == 'gauche' and matrix[start[0]][start[1]-1] == 1:
        # Si le serpent va vers la gauche et rencontre un mur, essayer de tourner en haut ou en bas
        if matrix[start[0]-1][start[1]] != 1:
            return ['haut'] + path
        elif matrix[start[0]+1][start[1]] != 1:
            return ['bas'] + path
    
    # Sinon, retourner le chemin tel quel
    return path
