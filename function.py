from queue import Queue
from PIL import Image, ImageOps
import numpy as np



def surround_matrix(matrix):
    m, n = matrix.shape
    surrounded = np.zeros((m + 2, n + 2), dtype=int)
    surrounded[1:-1, 1:-1] = matrix
    surrounded[0, :] = 1
    surrounded[:, 0] = 1
    surrounded[-1, :] = 1
    surrounded[:, -1] = 1
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
        for neighbor in get_neighbors(matrix, current):
            if neighbor not in path:
                q.put(neighbor)
                path[neighbor] = current

def get_neighbors(matrix, point):
    # Récupérer les coordonnées des voisins valides
    neighbors = []
    rows, cols = len(matrix), len(matrix[0])
    row, col = point
    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < rows and 0 <= c < cols and matrix[r][c] != 'X' and matrix[r][c] != 1:
            neighbors.append((r, c))
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