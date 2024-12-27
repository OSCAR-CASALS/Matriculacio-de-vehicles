# Matriculació de vehicles nous des del 2015 fins al 2023

## Autors

Òscar Casals Morro i Núria Solà Cases

## Descripció

Aquest dataset extreu de la web https://datosmacro.expansion.com/negocios/matriculaciones-vehiculos informació sobre les matriculacions i venta de vehicles mensuals i anuals pels països i anys indicats per l'usuari.

## Estructura

Aquest repositori està dividit en dos directoris, aquests són:

- **source**: conté els scripts que s'han utilitzat per generar el dataset, aquests són:

  * _1\_GetLatestNews.py_: Genera un txt amb les últimes notícies publicades a la web Datos Macro.

  * _2\_ExtractData.py_: Extreu de la web datos macro dades sobre els païssos i anys indicats per l'usuari.
  
  * _src/Functions.py_: Conté la funció ob_dades utilitzada per el script 2_ExtractData.py per extreure informació d'un país i any concret.
    
- **dataset**: Conté els resultats dels scripts pels païssos Alemania, Brasil, Espanya, Grècia, Irlanda, Itàlia i Reine Unit entre els anys 2015 i 2024, en concret té dos arxius:

  * _Ultimes_notícies.txt_: 8 últimes notícies publicades a DatosMacro.

  * _dataset_matriculacions_vehicles.csv_: Dades extretes pels païssos i anys corresponents.

- **requirements.txt**: Un artxiu de text amb les llibreries necessàries per executar el codi.

## DOI de Zenodo:

El dataset ha sigut publicat a Zenodo amb DOI: 

10.5281/zenodo.14066310

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14066310.svg)](https://doi.org/10.5281/zenodo.14066310)

## Utilització

Per crear un dataset primer s'ha d'executar el script _1\_GetLatestNews.py_ amb l'objectiu d'extreure el títol de les últimes notícies publicades a la web. Aquest programa requereix el nom d'un arxiu txt on es guardaran els resultats que posteriorment seran utilitzats per el script _2\_ExtractData.py_ per crear la columna Quantitat Notícies Recents.

Exemple:

```
python source/1_GetLatestNews.py dataset/Ultimes_notícies.txt
```

Un cop l'execució de _1\_GetLatestNews.py_ ha acabat, s'ha d'executar el script 2_ExtractData.py per generar el dataset final. Aquest script requereix els següents parametres:

- **-p**: Països que es volen incloure

- **-a**: Anys que es volen incloure.

- **-u**: Archiu txt generat per el script 1_GetLatestNews.py amb els títols de les últimes notícies publicades a https://datosmacro.expansion.com/negocios/matriculaciones-vehiculos

Opcionalment es pot especificar el csv on es guardaran els resultats, si no s'indica el archiu generat per el programa es dirà dataset_matriculacions_vehicles.csv. El paràmetre per especificar-ho és el següent:

- **-o**: CSV on es guardaren els resultats. 

Exemple:

```
python source/2_ExtractData.py -p "España" "Alemania" "Reino Unido" "Italia" "Irlanda" "Brasil" "Grecia" -a 2023 2022 2021 2020 2019 2018 2017 2016 2015 -u dataset/Ultimes_notícies.txt
```

## Execució utilitzada el dataset present en aquest repositori

En aquest repositori es troba un dataset amb informació dels països: España, Alemania, Reino Unido, Italia, Irlanda, Brasil, Grecia; i els anys: 2023, 2022, 2021, 2020. 2019, 2018, 2017, 2016, 2015.

Les comandes utilitzades són les següents:

```
python source/1_GetLatestNews.py dataset/Ultimes_notícies.txt
python source/2_ExtractData.py -p "España" "Alemania" "Reino Unido" "Italia" "Irlanda" "Brasil" "Grecia" -a 2023 2022 2021 2020 2019 2018 2017 2016 2015 -u dataset/Ultimes_notícies.txt
```
