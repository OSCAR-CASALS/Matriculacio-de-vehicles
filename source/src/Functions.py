##########################################################################################
# Important llibreries
##########################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

##########################################################################################
# Funció per extreure les dades d'un país i any concret en la web DatosMacro
##########################################################################################

def ob_dades(link):
    """
    Extreu de la web DatosMacro les següents dades per a un país i any concret:
        Any i mes en que es van recollir les dades, 
        Vehícles comerciales que es van matricular el Mes: , 
        Vehícles de passatgers que es van matricular el Mes, 
        Venta mensual de vehicles, 
        Vehícles que es van matricular al mes per cada 1000 habitants, 
        Vehicles comercials que es van vendre el Any, 
        Vehicles de passatgers que es van vendre el Any, 
        Venta anual de vehícles, 
        Vehícles que es van matricular al any per cada 1000 habitants.
    
    Args:
        link (string): Secció de la web DatosMacro d'on es volen extreure les dades.

    Returns:
        DataFrame: Un dataframe amb les dades extretes.
    """

    # En cas que la variable link estigui buida o no sigui del tipus adequat, llença un error.
    if (not link) or not isinstance(link, str):
         raise ValueError("El argument de la funció link està buit o no és un string.")

    # Concateneja el link donat com a argument amb el url de la web, aquesta variable conté el url de la web d'on
    # la funció extreura informació
    urlfin="https://datosmacro.expansion.com/"+link
    # Es fa una request al url creat anteriorment.
    pagefin=requests.get(urlfin)
    # A partir del HTML de la web anterior, es crea un objecte Beatiful Soup que s'utilitzarà per extreure informació.
    soupfin=BeautifulSoup(pagefin.content,'html.parser')
    # La taula amb id tb0_gth és la que té la informació d'interés, degut a això aquesta es guardada en una variable.
    table = soupfin.find("table", {"id": "tb0_gth"})
    # Per a que els noms de les columnes del dataframe que es retornarà com a resultat coincideixin amb els de la taula de la web, tots els elements th de
    # la web es guarden en una variable.
    headers=table.find_all("th")
    # Per a poder introduir els noms de columna en un dataframe, es treuen els espais en blanc de l'inici i final 
    # de les columnes, i són introduïts en una llista.
    wordheaders=[data.text.strip() for data in headers]
    # Es crea un dataframe amb les columnes.
    df=pd.DataFrame(columns=wordheaders)
    # Cada fila de la taula està conformada per elements tr amb la informació de cada columna en elements td, 
    # per extreure la informació de cada columna s'itera per cada fila de la taula extreient-hi el text present en 
    # els td. 
    rows=table.find("tbody").find_all("tr")  
    for row in rows:
          # S'obtenen els elements td de la fila per la qual s'està iterant.
          filadades=row.find_all("td")
          # Es crea una llista on cada element correspon a una columna.
          individual=[data.text.strip() for data in filadades]
          # S'afageix la llista anterior al dataframe que es donarà com a resultat.      
          df.loc[len(df)]=individual
    # Es retorna la informació obtinguda en un dataframe.
    return df