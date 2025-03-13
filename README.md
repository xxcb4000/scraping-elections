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
