# SAE15_Traiter_des_donn-es
📡 Cartographie des supports radioélectriques

Application interactive de visualisation et d'analyse des infrastructures radioélectriques développée avec Python, Pandas, Plotly et Dash.

🌍 Présentation du projet

Ce projet consiste à développer une application web interactive permettant de visualiser et d'analyser les supports radioélectriques à partir de plusieurs fichiers de données au format TXT.

Le programme regroupe différentes sources de données concernant les antennes, les stations, les supports, les propriétaires, les exploitants et la nature des infrastructures.

Après une phase de traitement et de nettoyage des données, celles-ci sont exploitées pour créer un tableau de bord composé d'un tableau interactif, de graphiques statistiques et d'une carte géographique.

L'objectif est de faciliter l'exploration des infrastructures radioélectriques et de mieux comprendre leur répartition géographique, administrative et temporelle.

🎯 Objectifs
Regrouper plusieurs fichiers de données dans un DataFrame unique.
Nettoyer et uniformiser les données collectées.
Convertir les coordonnées géographiques en degrés décimaux.
Visualiser la localisation des supports radioélectriques.
Analyser la répartition des supports selon leurs propriétaires et leurs utilisateurs.
Identifier les départements possédant le plus de supports.
Étudier les mises en service des supports depuis 2020.
Proposer une interface interactive facilitant la consultation des données.
🛠️ Technologies utilisées
Bibliothèque	Rôle
Python	Langage de programmation principal
Pandas	Importation, manipulation, fusion et nettoyage des données
Plotly Express	Création des graphiques et de la carte interactive
Dash	Création de l'application web
Dash AG Grid	Affichage et gestion du tableau interactif
Importations Python
python
from dash import Dash, html, dcc, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

📁 Organisation des fichiers

Le projet utilise deux dossiers contenant les fichiers de données nécessaires à son fonctionnement.

text
Projet/
│
├── data/
│   ├── sup_antenne.txt
│   ├── sup_station.txt
│   └── sup_support.txt
│
├── ref/
│   ├── sup_type_antenne.txt
│   ├── sup_proprietaire.txt
│   ├── sup_nature.txt
│   └── sup_exploitant.txt
│
├── main.py
│
└── README.md

Dossier data/

Contient les données principales utilisées pour décrire les infrastructures :

sup_antenne.txt : informations relatives aux antennes et à leur type.
sup_station.txt : informations relatives aux stations, aux exploitants et aux dates de mise en service.
sup_support.txt : informations relatives aux supports, notamment leur hauteur, leurs coordonnées géographiques, leur propriétaire et leur localisation.
Dossier ref/

Contient les fichiers de référence permettant d'enrichir les données principales :

sup_type_antenne.txt : correspondance des types d'antennes.
sup_proprietaire.txt : informations sur les propriétaires.
sup_nature.txt : informations sur la nature des supports.
sup_exploitant.txt : informations sur les exploitants.

Les fichiers sont au format TXT et utilisent le point-virgule (;) comme séparateur.

⚙️ Traitement des données

Le traitement des données est réalisé avec la bibliothèque Pandas et se déroule en plusieurs étapes.

1. Importation des fichiers

Les sept fichiers TXT sont importés dans des DataFrames distincts à l'aide de pd.read_csv().

Les données sont ensuite sélectionnées afin de ne conserver que les colonnes nécessaires au projet.

2. Fusion des DataFrames

Les différents DataFrames sont fusionnés à partir de leurs identifiants communs.

Les jointures utilisées sont des jointures gauches (how='left'), permettant de conserver les informations du fichier principal même lorsqu'une correspondance n'est pas trouvée dans un fichier de référence.

Les fusions sont réalisées dans l'ordre suivant :

Fusion des supports et des stations grâce à STA_NM_ANFR.
Ajout des informations relatives aux antennes.
Ajout des informations sur les exploitants grâce à ADM_ID.
Ajout de la nature des supports grâce à NAT_ID.
Ajout des propriétaires grâce à TPO_ID.
Ajout du type d'antenne grâce à TAE_ID.

Le résultat est un DataFrame unique nommé ssaenpt.

3. Conversion des coordonnées géographiques

Les coordonnées initiales sont exprimées au format degrés, minutes et secondes (DMS).

Afin de pouvoir les exploiter dans une carte interactive, elles sont converties en degrés décimaux.

La conversion utilise les formules suivantes :

Latitude :

python
latitude = (
    degres
    + minutes / 60
    + secondes / 3600
) * direction


Longitude :

python
longitude = (
    degres
    + minutes / 60
    + secondes / 3600
) * direction


Les directions géographiques sont prises en compte :

Direction	Valeur
Nord (N)	+1
Sud (S)	-1
Est (E)	+1
Ouest (W ou O)	-1

Les coordonnées obtenues sont arrondies à six décimales.

Les anciennes colonnes de coordonnées DMS sont ensuite supprimées pour ne conserver que latitude et longitude.

4. Nettoyage et vérification des données

Plusieurs opérations sont effectuées afin d'améliorer la qualité des données :

Conversion des coordonnées en valeurs numériques.
Conversion des hauteurs en valeurs numériques.
Remplacement des virgules décimales par des points dans les hauteurs.
Remplacement des hauteurs invalides ou manquantes par 1.
Remplacement des valeurs textuelles vides ou manquantes par Inconnu.
Création d'une colonne DEPARTEMENT à partir des deux premiers caractères du code postal.

Une nouvelle colonne HAUTEUR_NUM est créée afin de disposer d'une hauteur numérique exploitable pour la représentation cartographique.

5. Organisation finale des données

Une fois les traitements terminés, certaines colonnes techniques et identifiants devenus inutiles sont supprimés.

Les colonnes restantes sont renommées afin de rendre les informations plus compréhensibles et adaptées à l'affichage dans l'application.

📊 Fonctionnalités de l'application

L'application Dash propose plusieurs outils de consultation et d'analyse.

🔎 1. Tableau interactif et recherche

Un tableau interactif est créé grâce à Dash AG Grid.

Il permet de consulter l'ensemble des données traitées.

Ses fonctionnalités sont :

Recherche rapide dans les données grâce à une barre de recherche.
Tri des colonnes.
Filtrage des informations.
Redimensionnement des colonnes.
Pagination des résultats.

La pagination est configurée pour afficher 10 lignes par page.

La recherche est réalisée grâce à un callback Dash qui actualise la propriété quickFilterText du tableau en fonction du texte saisi par l'utilisateur.

👥 2. Top 10 des propriétaires

Un graphique en barres horizontales représente les dix propriétaires possédant le plus grand nombre de supports dans les données.

Il permet de visualiser les principaux propriétaires et de comparer leur nombre de supports.

🏢 3. Top 10 des utilisateurs

Ce graphique présente les dix utilisateurs ou exploitants possédant le plus grand nombre de supports recensés.

Il permet d'identifier les principaux acteurs utilisant les infrastructures radioélectriques.

🗺️ 4. Top 10 des départements

Un graphique en barres horizontales présente les dix départements ayant le plus grand nombre de supports.

Le département est déterminé à partir des deux premiers caractères du code postal.

📅 5. Évolution des mises en service depuis 2020

Un graphique chronologique représente le nombre de supports mis en service depuis le 1er janvier 2020.

Les dates sont converties au format datetime grâce à pd.to_datetime().

Les données sont ensuite regroupées par date de mise en service afin de calculer le nombre de supports concernés pour chaque date.

Le graphique est réalisé avec px.line() et comporte des marqueurs pour faciliter la lecture des données.

📍 6. Cartographie interactive des supports radioélectriques

La carte est créée avec px.scatter_map() à partir des coordonnées géographiques calculées précédemment.

Chaque point représente un support radioélectrique.

La taille des points varie en fonction de la hauteur du support.

Le regroupement automatique des points (cluster) permet d'améliorer la lisibilité de la carte lorsque plusieurs infrastructures sont proches les unes des autres.

Au survol d'un point, les informations suivantes sont affichées :

Lieu d'implantation.
Date de mise en service.
Hauteur du support.
Code postal.
Propriétaire.
Type de support.
Type d'antenne.
Exploitant.

La carte est également configurée avec une hauteur de 800 pixels.

🚀 Installation et lancement
1. Prérequis

Pour utiliser le projet, il est nécessaire de disposer de :

Python 3 installé sur l'ordinateur.
pip pour installer les bibliothèques Python.
Tous les fichiers TXT présents dans les dossiers data/ et ref/.
2. Installation des bibliothèques

Ouvrir un terminal dans le dossier du projet et exécuter la commande suivante :

bash
pip install pandas dash dash-ag-grid plotly

3. Lancement du programme

Exécuter le fichier Python principal :

bash
python main.py


Le programme effectue automatiquement les opérations suivantes :

Importation des fichiers de données.
Fusion des différents DataFrames.
Conversion et nettoyage des coordonnées.
Vérification et nettoyage des données.
Création des graphiques statistiques.
Création de la carte interactive.
Lancement de l'application Dash.

L'application est accessible depuis un navigateur à l'adresse :

text
http://127.0.0.1:8050/


Le programme ouvre également la carte Plotly dans un navigateur grâce à carte.show(renderer="browser").

⚠️ Limites et précautions

Quelques éléments doivent être pris en compte lors de l'utilisation de l'application :

Les données affichées dépendent directement des fichiers TXT fournis.
Les supports dont les coordonnées sont absentes ou invalides ne peuvent pas être correctement géolocalisés.
Les hauteurs invalides sont remplacées par 1, ce qui ne correspond pas nécessairement à leur hauteur réelle.
Les valeurs manquantes sont remplacées par Inconnu dans les colonnes textuelles.
L'extraction du département repose sur les deux premiers caractères du code postal. Cette méthode ne gère pas correctement tous les cas particuliers, notamment les départements corses et certains territoires ultramarins.
Le graphique des mises en service ne prend en compte que les dates à partir du 1er janvier 2020.
🔮 Améliorations possibles

Plusieurs évolutions pourraient être envisagées pour compléter l'application :

Ajouter des filtres interactifs pour affiner les données affichées sur la carte.
Permettre de filtrer les supports selon leur propriétaire, leur exploitant ou leur département.
Ajouter des statistiques globales : nombre total de supports, hauteur moyenne et répartition par type.
Améliorer la gestion des départements corses et ultramarins.
Ajouter une fonctionnalité d'exportation des données au format CSV ou Excel.
Améliorer l'organisation et le design de l'interface Dash.
❤️ Conclusion

Ce projet permet de transformer plusieurs fichiers de données brutes en une application interactive dédiée à la visualisation et à l'analyse des supports radioélectriques.

Grâce à Pandas, les données sont regroupées, nettoyées et enrichies. Plotly Express permet ensuite de créer des visualisations statistiques et géographiques, tandis que Dash offre une interface web permettant de consulter facilement les résultats.

Ce projet met en pratique plusieurs compétences en programmation Python, en traitement de données, en géolocalisation et en développement d'applications web interactives.

<p align="center">
**Développé avec Python 🐍, Pandas 🐼, Plotly 📊 et Dash ⚡**
**Développé par Saurel Marien, Ignazi Nigel, Bayindir Faruk, Agaba James**
</p>