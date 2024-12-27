##########################################################################################
# Aquest script té l'objectiu de extreure les 8 últimes notícies publicades a la web DatosMacro
# per utilitzarlas com a mesura de que tan rellevant és el país del qual s'extreuen les dades.
#
# Aquest programa genera un archiu de text amb les 8 últimes notíces publicades a la web DatosMacro
##########################################################################################

##########################################################################################
# Important llibreries
##########################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import sys

##########################################################################################
# Comprovant que els parametres requerits per el script s'hagin introduit
##########################################################################################

# Si no hi ha un argument que indiqui el archiu on es guardaran els resultats, indica al usuari que s'ha d'especificar.
if len(sys.argv) == 1:
    print("El archiu on es guardaran els resultats s'ha d'especificar.", "Per exemple:", "python 1_GetLatestNews.py Ultimes_notícies.txt", sep = "\n")
    sys.exit()
# El archiu on es guardaran els resultats correspon al primer argument que es dona al script.
OutputFile = sys.argv[1]

##########################################################################################
## Es navega cap a la web del nostre interés
##########################################################################################

# S'inicialitza el webdriver 
driver = webdriver.Chrome()
# Es navega fins a la web del nostre interés. Las últimes notícies són sempre les mateixes, podem extreure-les només
# un cop per un país en concret.
driver.get("https://datosmacro.expansion.com/negocios/matriculaciones-vehiculos/espana")

try:
    ##########################################################################################
    # Cookies 
    ##########################################################################################

    # Abans de poder interactuar amb la web, s'han d'acceptar les cookies per a que es pugui accedir a
    # la pròpia web. Per fer això primer el script s'espera a que aparegui el botó d'acceptar les cookies i després
    # li dona click.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ue-accept-notice-button"))).click()

    ##########################################################################################
    # Extracció d'informació
    ##########################################################################################
    
    # Abans d'extreure informació el script s'esperà a que el element amb la informació que volem extreure aparegui.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lastcar")))
    
    # Es guarda el botó encarregat de decidir quines noticies es mostren en una variable.
    next_button = driver.find_element(By.CSS_SELECTOR, ".bottom-control.float-end")
    # Es crea el arxiu que contindrà les noticies més recents.
    file = open(OutputFile, "w+")

    for i in range(4):
        # Es guarda el element amb les dades que volem extreure en una variable
        carousel = driver.find_element(By.ID, "lastcar")
        # S'identifica el element amb la informació que ens interesa. Aquest element canvia cada cop que es fa click al botó
        # dintre de la variable next_button per tant aquesta variable s'haurà d'actualitzar cada cop que es fagi click al botó.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "carousel-item.active")))
        active_item = carousel.find_element(By.CLASS_NAME, "carousel-item.active")
        # Dintre del element amb classe "carousel-item.active" es troba un element amb classe "list-news-tit" que poseeix el títol
        # de les últimes notícies publicades a la web, és a dir, el que volem extreure. Per tant el guardem en una variable.
        news_items = active_item.find_elements(By.CLASS_NAME, "list-news-tit")
        # Iterant per cada notícia al element guardat a "news_items" s'obtenen els títols de diverses notícies, aquest títols són exportats
        # a un arxiu txt.
        for item in news_items:
            headline = item.text
            print("- ", headline, file = file)
                
        # Es comprova que el botó per canviar de notícia és clicable.
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(next_button))
        # Fes scroll al header de lastcar per asegurar que next_button sempre sigui visible
        block = driver.find_element(By.ID, "block-block-8")
        driver.execute_script("arguments[0].scrollIntoView(true);", block)
        # Abans de clicar el butó, el programa s'espera 1 segon.
        time.sleep(1)
        # Es clica el butó per canviar de notícies.
        next_button.click()
            
            
    # Es tanca el webdriver
    driver.quit()
    # Es tanca el arxiu que conté els resultats.
    file.close()


except Exception as e:
    # En cas que es doni un error, imprimeix el error en pantalla i tanca el webdriver.
    print("Error ocurred:", e)
    driver.quit()
