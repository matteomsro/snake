from selenium import webdriver
from PIL import*
from io import BytesIO
from function import*
import numpy as np
import time
from PIL import ImageDraw
from PIL import ImageFont

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

start_time = time.time()
lit =[]
i=0
# Code à exécuter pendant 60 secondes
timelist = []
while True:

    start_time1 = time.time()

    start_time = time.time()
    # instructions à exécuter ici
    # Remplir un formulaire
    driver.get_screenshot_as_file("screenshot.png")
    #driver.get_screenshot_as_file("screenshot" + str(i) + ".png")


    # Enregistrer le temps de fin d'exécution
    end_time = time.time()

# Calculer le temps d'exécution
    timelist.append(("screen",end_time - start_time))


    start_time = time.time()
    # Ouvrir l'image
    image = Image.open("screenshot.png")

    width, height = image.size
    # Recadrer l'image
    image = image.crop((width*0.05, height*0.15, width*0.445, height*0.88))

    # Chargez l'image et convertissez-la en mode RVB
    image = image.convert("RGB")

    # Convertir l'image en un tableau NumPy pour une manipulation rapide des pixels
    pixels = np.array(image)

    
    # Définir le seuil de tolérance pour les composantes rouge et verte
    tolerance = 100

    # Créer un masque de pixels à garder, basé sur les pixels blanc et rouge
    mask = ((pixels[:,:,0] >= 255-tolerance) & (pixels[:,:,1] <= tolerance) & (pixels[:,:,2] <= tolerance)) | ((pixels[:,:,0] >= 255-tolerance) & (pixels[:,:,1] >= 255-tolerance) & (pixels[:,:,2] >= 255-tolerance))

    # Appliquer le masque pour rendre tous les pixels non-rouge / non-blanc transparents
    pixels[~mask] = [0, 0, 0]

    end_time = time.time()

    timelist.append(("enleverpixel",start_time - end_time))


    start_time = time.time()

    # Définir le seuil de tolérance pour la détection des couleurs (20%)
    tolerance = 0.2

    # Trouver les pixels blancs
    indices_blanc = np.where(np.all(pixels >= 255 * (1 - tolerance), axis=-1))

    if indices_blanc[0].size > 0:
        # Calculer la moyenne des positions des pixels blancs
        moyenne_blanc = np.mean(np.array([indices_blanc[0], indices_blanc[1]]), axis=1)
        pos_tete=(round(15*moyenne_blanc[0]/569)+1,round(17*moyenne_blanc[1]/614)+1)

    # Trouver les pixels rouges
    rouge_bas = np.array([255 * (1 - tolerance), 0, 0])
    rouge_haut = np.array([255, 255 * (1 - tolerance), 255 * (1 - tolerance)])

    indices_rouge = np.where(np.all((pixels >= rouge_bas) & (pixels <= rouge_haut), axis=-1))

    if indices_rouge[0].size > 0:
        # Calculer la moyenne des positions des pixels rouges
        moyenne_rouge = np.mean(np.array([indices_rouge[0], indices_rouge[1]]), axis=1)
        pos_pomme=(round(15*moyenne_rouge[0]/569),round(17*moyenne_rouge[1]/614)+1)
    
    tableau = np.zeros((15, 17))

    end_time = time.time()

    timelist.append(("pos", start_time - end_time))

 

    
    


    liste = find_path(tableau,pos_tete,pos_pomme)

    
    lit.append((i,pos_tete,pos_pomme,liste))
    start_time = time.time()
    if len(liste)>0:
        actions.send_keys([dict[elt] for elt in liste]).perform()
        

    end_time = time.time()

    timelist.append(("instruc",start_time - end_time))


    start_time = time.time()
    
    
    # Créer un objet Draw pour dessiner sur l'image
    draw = ImageDraw.Draw(image)

    # Définir la police de caractères et la taille du texte
    font = ImageFont.truetype("arial.ttf", 20)

    # Définir la position et le contenu du texte à écrire
    texte = str(lit[i])
    position = (10, 10)

    # Écrire le texte sur l'image
    draw.text(position, texte, fill=(0), font=font)

    # Enregistrer l'image modifiée
    image.save("screenshot" + str(i) + ".png")
    
    i+=1

    end_time=time.time()

    
    timelist.append(("ecriture",start_time - end_time,"final",start_time1 - end_time))
    
    print("ici",timelist)
    
    # Sortir de la boucle après 60 secondes
    if time.time() > start_time + 60:
        break


driver.close()