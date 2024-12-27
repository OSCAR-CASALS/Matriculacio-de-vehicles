##########################################################################################
# Important llibreries
##########################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import argparse

from src.Functions import ob_dades

##########################################################################################
## Agafant paràmetres del usuari
##########################################################################################
# S'inicialitza la llibreria argparse per agafar els arguments donats per el usuari.
parser = argparse.ArgumentParser(description="Recopila informació relacionada amb la matriculació de vehicles nous per els païssos i anys introduits.")

# Es defineixen els diferents parametres que pot definir el usuari.
parser.add_argument("-p","--paisos", nargs="+", type=str, required=True, help="Països per als quals s'extreurà informació")
parser.add_argument("-a","--anys", nargs="+", type=str, required=True, help="Anys per als quals es recopilarà informació")
parser.add_argument("-u", "--UltimesNoticies", type=str, required=True, help="Archiu txt amb els títols de les últimes notícies publicades ")
parser.add_argument("-o", "--output", type=str, required=False, default="dataset_matriculacions_vehicles.csv", help="CSV on es guardaren els resultats, per defecte es dirà dataset_matriculacions_vehicles.csv")
args = parser.parse_args()

# Els Països escrits per l'usuari es guarden a la variable Paisos
Paisos = args.paisos

# Els anys especificats per l'usuari es guarden a la variable Anys.
Anys = args.anys

##########################################################################################
## Carregant últimes notícies
##########################################################################################

# Amb el script 1_GetLatesNews.py s'han extret les 8 últimes notícies publicades a DatosMacro, aquestes
# dades s'utilitzaran més endavant com a mesura de la relevància actual dels països inclosos en la data.

# Amb aquesta instrucció s'obre el txt generat amb read-only mode.
LastNews = open(args.UltimesNoticies, mode = "r")

# Es crea una llista amb totes les líneas del txt
LatestNews = LastNews.readlines()

# Com ja no fa falta seguir treballant amb l'arxiu obert, es tanca.
LastNews.close()

# Aquesta llista contindrà cada paraula en el txt, aquesta variable s'utilitzarà més endavant per comptar quantes vegades
# surt el nom d'un país.
WordsLatestNews = []

# En aquest loop per cada línia: es treu el final de línia, es posa tota la lletra en minúscula, i es separen les paraules.
for i in range(0, len(LatestNews) - 1):
    WordsLatestNews += LatestNews[i].replace("\n", "").lower().split(" ")


##########################################################################################
## Recopilació de dades i creació de DataFrame
##########################################################################################

# La url de la web d'on s'extreuran les dades.
url="https://datosmacro.expansion.com/negocios/matriculaciones-vehiculos"

# Aquest Data Frame Contindrà els resultats extrets per cada país
df = pd.DataFrame()

# Es fa una request a la pàgina web amb l'objectiu de extreure dades.
page=requests.get(url)

# Es crea un objecte BeautifulSoup a partir del HTML de la pàgina.
soup=BeautifulSoup(page.content,'html.parser')

# A la web hi ha una taula que, en cada filera, té un url a les dades que cada 
# país té per tots els anys registrats a la web. Amb la següent instrucció s'extreu el div
# que conté la taula.
table = soup.find("div",class_="table-responsive")
    
# La taula amb id tb1 conté en cada una de les seves files un element "anchor" que porta a les dades que volem extreure,
# amb aquesta instrucció s'extreuen tots els "anchor" de la taula. 

u = table.find(id="tb1").find("tbody").find_all("a")

# Com els elements anchor de la taula poseeixen el nom del país en l'atribut títol, s'itera per cadascun d'ells i quan es troba un amb el país en títol,
# es fa una request el url i s'extreuen les dades amb la funció ob_dades.

# Per mirar si tots els països introduïts per l'usuari s'han trobat, es crea un contador.
count = 0

for i in u:
    if  i.get("title").split(" - ")[0] in Paisos:
        Pais = i.get("title").split(" - ")[0]
        print("Extreïent informació de:", Pais)
        # La web conté per cada país dades per diversos anys, cadascuna amb la seva pròpia url.
        # Com aquesta url cesta composta per la url amb les dades del país amb la terminació ?ani=ANY(on ANY correspon a l'any en el que es van extreure les dades),
        # concatenant el url del país del nostre interés amb els anys que volem analitzar podem obtenir les dades que es van registrar en els anys que s'han indicat com a input.
        for year in Anys:
            # Abans de fer una request, el programa s'espera 5 segons per no sobrecarregar la web.
            time.sleep(4)
            # Es crea un dataframe amb les dades corresponents al país i any per al qual s'està iterant.
            a = ob_dades(i.get("href") + "?anio=" + year)
            # Es crea una columna per identificar el país al qual corresponen les dades obtingudes 
            a.insert(0, "País", [Pais] * a.shape[0])
            # Es crea una columna amb la quantitat de notícies recents del país per al qual s'està iterant.
            a["Quantitat.Notícies.Recents"] = [WordsLatestNews.count(Pais.lower())] * a.shape[0]
            # Es concateneja el dataframe obtingut amb el dataframe que conté les dades dels altres països per als quals s'ha iterat.
            df = pd.concat([df,a])
        count += 1

# En cas que hi hagin paisos que no s'hagin trobat a la web, es notifica a l'usuari.
if count < len(Paisos):
    print("Hi han Països que no s'han trobat a la web https://datosmacro.expansion.com/negocios/matriculaciones-vehiculos")


##########################################################################################
## Preparació del resultat
##########################################################################################

# Es tradueixen els noms de cada columna al català.
df = df.rename(columns={
                   "Fecha": "Data",
                   "Vehículos comerciales Mes": "Vehicles Comercials Mes",
                   "Vehículos pasajeros Mes": "Vehicles Passatgers Mes",
                   "Venta mensual vehículos": "Venta Mensual vehicles",
                   "Vehículos Mes/1000 hab.": "Vehicles Mes/1000 hab.",
                   "Vehículos comerciales Año": "Vehicles Comercials Any",
                   "Vehículos pasajeros Año": "Vehicles Passatgers Any",
                   "Venta anual vehículos": "Venta Anual vehicles",
                   "Vehículos Año/1000 hab.": "Vehicles Any/1000 hab."
                   })

# Es separa la columna Data en dues, una per l'any i l'altre per el mes
df[["Mes", "Any"]] = df["Data"].str.split(" ", expand=True)

# S'elimina la columna Data per evitar informació redundant
df = df.drop("Data", axis=1)
# Per comoditat de lectura es mouen les columnes Mes i Any a les posicions 2 i 3 del dataframe.
cols = df.columns.tolist()

cols = cols[:1] + ["Mes", "Any"] + cols[1:-2]

df = df[cols]

##########################################################################################
## Exportació a CSV.
##########################################################################################

# S'exporta el datframe obtingut a csv.
df.to_csv(args.output, sep = ";", index = False)
