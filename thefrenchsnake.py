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
driver.execute_script("document.body.style.zoom='80%'")


time.sleep(2)

# Créer une instance de la classe ActionChains
actions = ActionChains(driver)

# Simuler l'appui sur la touche espace
actions.send_keys(Keys.SPACE).perform()

time.sleep(2)

actions.send_keys(Keys.RIGHT).perform()

time.sleep(2)
# Remplir un formulaire
driver.get_screenshot_as_file("screenshot.png")


time.sleep(1)


# Ouvrir l'image
image = Image.open("screenshot.png")

width, height = image.size
# Recadrer l'image
image = image.crop((width*0.05, height*0.15, width*0.45, height*0.9))

# Pixeliser l'image
pixel_size = 35
image = image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
image = image.resize((image.width, image.height), Image.NEAREST)

# Enregistrer l'image pixelisée


# Convertir l'image en niveau de gris
image = image.convert("L")
image.save("pixelated_image.png")

# Obtenir la matrice de pixels
pixel_matrix = np.array(Image.open("pixelated_image.png"))
pixel_matrix = np.where((pixel_matrix >= 130) & (pixel_matrix <= 250), 0, pixel_matrix)




# Afficher la matrice
print(pixel_matrix)

driver.close()