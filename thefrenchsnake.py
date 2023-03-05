from selenium import webdriver
from PIL import Image
from io import BytesIO
from function import*
import numpy as np



import time

# Attendre 5 secondes avant de fermer le navigateur


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


dict = {"haut":Keys.UP,"bas":Keys.DOWN,"gauche":Keys.LEFT,"droite":Keys.RIGHT}
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

time.sleep(1)


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


# Convertir l'image en niveau de gris

image.save("pixelated_image.png")


# Convertir l'image en un tableau NumPy
image_array = np.array(image)

# Extraire le canal rouge de l'image
red_channel = image_array[:,:,0]

print(red_channel)



# Trouver les deux valeurs les plus grandes
max_vals = np.partition(red_channel.flatten(), -2)[-2:]


# Trouver les positions des deux valeurs les plus grandes
pos_pomme_i = np.where(red_channel == max_vals[0])
pos_pomme = list(zip(pos_pomme_i[0], pos_pomme_i[1]))
pos_tete_i = np.where(red_channel == max_vals[1])
pos_tete = list(zip(pos_tete_i[0], pos_tete_i[1]))


print(pos_tete,pos_pomme)
list = find_path(red_channel,pos_tete[0],pos_pomme[0])
print(list)
for elt in list:
    actions.send_keys(dict[elt]).perform()
    time.sleep(2)



driver.close()