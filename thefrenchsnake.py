from selenium import webdriver
from PIL import Image
from io import BytesIO
import numpy as np


import time

# Attendre 5 secondes avant de fermer le navigateur


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Créer une instance du navigateur Chrome
driver = webdriver.Chrome()

# Accéder à une URL
driver.get('https://www.google.com/fbx?fbx=snake_arcade')


time.sleep(5)

# Créer une instance de la classe ActionChains
actions = ActionChains(driver)

# Simuler l'appui sur la touche espace
actions.send_keys(Keys.SPACE).perform()

time.sleep(5)


# Remplir un formulaire
driver.get_screenshot_as_file("C:/Users/Estudiante/Downloads/screenshot.png")


time.sleep(5)


# Ouvrir l'image
image = Image.open("C:/Users/Estudiante/Downloads/screenshot.png")

# Convertir l'image en tableau numpy
pixel_array = np.array(image)

# Afficher la forme de la matrice (largeur x hauteur x 3)
print(pixel_array.shape)

# Accéder aux valeurs des pixels
print(pixel_array)  # Affiche le pixel en haut à gauche
# Fermer le navigateur
driver.close()