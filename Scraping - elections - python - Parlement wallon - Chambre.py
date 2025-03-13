"""
Nous voulons mener des analyses sur les résultats des élections en Wallonie en 2019 et en 2024. 
Nous visons, dans une première étape, à créer une collection de dictionnaires json,
un dictionnaire par commune avec les résultats des élections au Parlement wallon
et à la Chambre en 2019 et en 2024. Voici à quoi devrait ressembler le fichier :

"Commune": {
    "élections PW 2024": {
        "Parti 1": "résultat parti 1 en %",
        "Parti 2": "résultat parti 2 en %",
        "...": "..."
    },
    "élections PW 2019": {
        "Parti 1": "résultat parti 1 en %",
        "Parti 2": "résultat parti 2 en %",
        "...": "..."
    },
    "élections CHAMBRE 2024": {
        "Parti 1": "résultat parti 1 en %",
        "Parti 2": "résultat parti 2 en %",
        "...": "..."
    },
    "élections CHAMBRE 2019": {
        "Parti 1": "résultat parti 1 en %",
        "Parti 2": "résultat parti 2 en %",
        "...": "..."
    }

Les résultats sont stockés par exemple sur le site https://elections2024.belgium.be/ du SPF intérieur. 
On y trouvera les résultats des élections au Parlement wallon et à la Chambre en 2024 et en 2019, 
c'est ce que nous cherchons. 
Cette première étape de construction de notre fichier est donc une étape de scraping. 
Nous allons scraper le site en python en utilisant les librairies requests (pour les requêtes http),
beautifullsoup (pour identifier mes balises dans le dom qui me permettront d'aller isoler les infos que
je souhaite récuperer), urllib3 (pour éviter un avertissement SSL, il n'y aura aucun échange d'information sensible...
à ne pas faire en production) et json (pour écrire mon fichier). 
Nous avons choisi la granularité communale pour notre liste de dictionnaires json. 
Elle devrait nous permettre de mener des analyses par commune, par arrondissement, par district ou par province. 
Á ce stade, nous n'irons pas chercher les résultats des élections antérieures, ni les résultats des
élections communales ou provinciales, ni les scores individuels des candidats. On pourrait prolonger le travail 
de ce côté-là dans un temps ultérieur. 
Enfin, j'ai utilisé pprint pour des affichages plus friendly en cours de développement, et html.unescape 
pour aller chercher le texte brut dans mes balises html.

C'est parti ! 
"""


# Le site web est organisé par circonscription. Pour retrouver les résultats au niveau des communes,
# on doit passer par les circonscriptions plus larges. Nous allons privilégier l'approche par canton. 
# Donc... nous devons procéder en 3 temps pour chaque type d'élections :
# - collecter les URL des cantons ;
# - parcourir les pages des cantons et aller chercher les URL des communes dans le menu déroulant (option) ;
# - parcourir les pages de communes et scraper les résultats 2024 et 2019. 
# C'est la même approche pour le Parlement wallon et pour la Chambre. 
# Allons-y !


#############################################################################
# Construire un json avec les URL des résultats par commune (Chambre)       #
#############################################################################

import requests
from bs4 import BeautifulSoup
import urllib3
import json
from pprint import pprint
import html

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# On commence par la Chambre. Avec requests. Et on le beautifulsoup. 
URL = 'https://elections2024.belgium.be/fr/election?el=CK'
response = requests.get(URL, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
# On va chercher les balises de lien dans mon dom. 
balises_a = soup.find_all('a')

# Je prépare ma liste de dictionnnaires pour les URL des cantons. 
circonscriptionsURL= {}

# Je reconstruis les URL des cantons à partir du contenu de mes href quand mes balises comportent le mot "Canton". 
for balise in balises_a:
    if ('href' in balise.attrs) and (balise.find('dt')) and ('Canton' in balise.find('dt').get_text()):
            circonscription = balise.find('dt').get_text()
            circonscriptionsURL[circonscription] = f"https://elections2024.belgium.be{balise['href']}"

# Petite vérif
pprint(circonscriptionsURL)    

# Je prépare ma liste de dictionnaires pour les URL des communes. 
communesURL= {}

# Je vais parcourir les URL des cantons. 
for URL in circonscriptionsURL.values():
    response = requests.get(URL, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
# Je cherche l'endroit de la page où je trouverai les résultats communaux.
    balises_a = soup.find('a', string='Résultats communaux')
# Si la chaine de caractères existe, alors je vais voir la page correspondante. 
    if balises_a is not None:
        balises_a = html.unescape(f"https://elections2024.belgium.be{balises_a['href']}")
        response = requests.get(balises_a, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
# Et je vais chercher les URL des pages des résultats par commune. Dans le menu déroulant. 
        balises_a_communes = soup.findAll('option')
# Je reconstruis les URL avec le contenu des balises "option"
        for baliseOption in balises_a_communes[3:]:
            commune = baliseOption.get_text()
            communesURL[commune] = html.unescape(f"https://elections2024.belgium.be{baliseOption['value']}") 
        print(f"Collecte URL de {commune}")

# Petite vérification en passant. 
pprint(communesURL)
      
# Je charge ma liste d'URL dans un json
with open("listeURLcommunesCHAMBRE2024.json", 'w', encoding='utf-8') as f:
 json.dump(communesURL, f, ensure_ascii=False, indent=4)


######################################################################################
# Construire un json avec les URL des résultats par commune (Parlement wallon)       #
######################################################################################


# Exactement les mêmes étapes. 

import requests
from bs4 import BeautifulSoup
import urllib3
import json
from pprint import pprint
import html

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = 'https://elections2024.belgium.be/fr/election?el=WL'
response = requests.get(URL, verify=False)

soup = BeautifulSoup(response.text, 'html.parser')

balises_a = soup.find_all('a')


circonscriptionsURL= {}


for balise in balises_a:
    if ('href' in balise.attrs) and (balise.find('dt')) and ('Canton' in balise.find('dt').get_text()):
            circonscription = balise.find('dt').get_text()
            circonscriptionsURL[circonscription] = f"https://elections2024.belgium.be{balise['href']}"


pprint(circonscriptionsURL)    

communesURL= {}

for URL in circonscriptionsURL.values():
    response = requests.get(URL, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    balises_a = soup.find('a', string='Résultats communaux')
    balises_a = html.unescape(f"https://elections2024.belgium.be{balises_a['href']}")

    response = requests.get(balises_a, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    balises_a_communes = soup.findAll('option')

    for baliseOption in balises_a_communes[3:]:
        commune = baliseOption.get_text()
        communesURL[commune] = html.unescape(f"https://elections2024.belgium.be{baliseOption['value']}") 
    print(f"Collecte URL de {commune}")

pprint(communesURL)

with open("listeURLcommunesPW2024.json", 'w', encoding='utf-8') as f:
 json.dump(communesURL, f, ensure_ascii=False, indent=4)



 # Bon, j'ai mes deux json avec mes URL qui pointent vers les résultats par commune. 
 # On va donc parcourir ces URL. 

#################################################
# Parcourir mes URL et scraper les résulats     #
#################################################

# Je ne vais par réepliquer toutes les étapes. 
# Juste celles qui nécessitent un petit mot d'explication. 
# Je commence par le Parlement wallon.

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import certifi
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('listeURLcommunesPW2024.json', 'r') as f:
    communesURL = json.load(f)

pprint(communesURL)

élections = "élections PW 2024"
électionsprécédentes = "élections PW 2019"

# Voici ma variable qui va recevoir toutes les infos : 
datasetscrapelec = {}

for nomCommune, URLcommune in communesURL.items():
    response = requests.get(URLcommune, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f'Scraping {nomCommune}')
# Voici la structure attendue de ma liste de dictionnaires json
# Bien noter que les résultats 2019 sont accessibles sur le site des résultats 2024. 
# S'il fallait remonter à 2014 et avant, il faudrait aller chercher sur un autre site, un autre URL. 
    datasetscrapelec[nomCommune] = {}
    datasetscrapelec[nomCommune][élections] = {}
    datasetscrapelec[nomCommune][électionsprécédentes] = {}

    politique_container = soup.find('tbody', class_='table__body')
# Le tout c'est de bien identifier dans le dom les balises qui permettent d'isoler le nom des partis et leurs résultats
# Le site est organisé sous forme de tableau (tr, td). 
    for trlist in politique_container:
        tdlist = trlist.find_all('td') 
        parti = tdlist[1].text
        résultat = tdlist[5].text
        résultatprécédent = tdlist[6].text
        datasetscrapelec[nomCommune][élections][parti] = résultat
        datasetscrapelec[nomCommune][électionsprécédentes][parti] = résultatprécédent


with open("scrapeleccommunes.json", 'w', encoding='utf-8') as f:
    json.dump(datasetscrapelec, f, ensure_ascii=False, indent=4)

# Je vais faire une sauvegarde du fichier : DATASET - COMMUNES (v.elecPW2024-2019).json
# Je passe à la Chambre. 

with open('listeURLcommunesCHAMBRE2024.json', 'r') as f:
    communesURL = json.load(f)
with open('DATASET - COMMUNES (v.elecPW2024-2019).json', 'r') as f:
    datasetscrapelec = json.load(f)

pprint(communesURL)

élections = "élections CHAMBRE 2024"
électionsprécédentes = "élections CHAMBRE 2019"

# je n'ai plus besoin de recréer ma variable datasetscrapelec puisque j'ai chargé le json du Parlement wallon

for nomCommune, URLcommune in communesURL.items():
    if nomCommune in datasetscrapelec:
        response = requests.get(URLcommune, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Scraping {nomCommune}')
# je crée les sections du dictionnaire dans lesquelles je vais venir charger mes résultats
        datasetscrapelec[nomCommune][élections] = {}
        datasetscrapelec[nomCommune][électionsprécédentes] = {}

        politique_container = soup.find('tbody', class_='table__body')

        for trlist in politique_container:
            tdlist = trlist.find_all('td') 
            parti = tdlist[1].text
            résultat = tdlist[5].text
            résultatprécédent = tdlist[6].text
            datasetscrapelec[nomCommune][élections][parti] = résultat
            datasetscrapelec[nomCommune][électionsprécédentes][parti] = résultatprécédent

    print(nomCommune)
    

with open("scrapeleccommunes PW et CHAMBRE.json", 'w', encoding='utf-8') as f:
    json.dump(datasetscrapelec, f, ensure_ascii=False, indent=4)

"""
Et voilà. J'ai un json avec, pour chaque commune, les résultats par parti aux élections fédérales
et régionales en 2019 et en 2024. 

Par exemple Liège : 

"Liège": {
    "élections PW 2024": {
        "MR": "20,51%",
        "PS": "26,41%",
        "LES ENGAGÉS": "13,68%",
        "CDH": "-",
        "PTB": "19,36%",
        "DéFI": "2,63%",
        "ECOLO": "11,36%",
        "Collectif Citoyen": "1,71%",
        "CHEZ NOUS": "3,70%",
        "RMC": "0,64%",
        "PARTI POPULAIRE": "-",
        "LISTES DESTEXHE": "-",
        "DierAnimal": "-",
        "NATION": "-",
        "Wallonie Insoumise": "-",
        "DEMAIN": "-"
    },
    "élections PW 2019": {
        "MR": "14,83%",
        "PS": "26,28%",
        "LES ENGAGÉS": "-",
        "CDH": "6,27%",
        "PTB": "19,02%",
        "DéFI": "4,17%",
        "ECOLO": "18,98%",
        "Collectif Citoyen": "1,02%",
        "CHEZ NOUS": "-",
        "RMC": "-",
        "PARTI POPULAIRE": "3,21%",
        "LISTES DESTEXHE": "1,81%",
        "DierAnimal": "1,75%",
        "NATION": "0,67%",
        "Wallonie Insoumise": "0,87%",
        "DEMAIN": "1,13%"
    },
    "élections CHAMBRE 2024": {
        "MR": "20,61%",
        "PS": "24,07%",
        "LES ENGAGÉS": "12,69%",
        "CDH": "-",
        "PTB": "20,37%",
        "N-VA": "1,31%",
        "DéFI": "2,49%",
        "ECOLO": "11,65%",
        "Collectif Citoyen": "1,42%",
        "BELG.UNIE-BUB": "0,24%",
        "BLANCO": "1,76%",
        "CHEZ NOUS": "2,88%",
        "RMC": "0,50%",
        "PARTI POPULAIRE": "-",
        "VLAAMS BELANG": "-",
        "LISTES DESTEXHE": "-",
        "DierAnimal": "-",
        "LA DROITE": "-",
        "LES BELGES D'ABORD": "-",
        "NATION": "-",
        "WALLONIE INSOUMISE": "-"
    },
    "élections CHAMBRE 2019": {
        "MR": "15,43%",
        "PS": "24,78%",
        "LES ENGAGÉS": "-",
        "CDH": "5,58%",
        "PTB": "19,10%",
        "N-VA": "-",
        "DéFI": "3,82%",
        "ECOLO": "20,72%",
        "Collectif Citoyen": "1,05%",
        "BELG.UNIE-BUB": "-",
        "BLANCO": "-",
        "CHEZ NOUS": "-",
        "RMC": "-",
        "PARTI POPULAIRE": "2,75%",
        "VLAAMS BELANG": "0,48%",
        "LISTES DESTEXHE": "1,60%",
        "DierAnimal": "1,60%",
        "LA DROITE": "0,54%",
        "LES BELGES D'ABORD": "1,55%",
        "NATION": "0,44%",
        "WALLONIE INSOUMISE": "0,56%"
    }



"""