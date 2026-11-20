# SAE15_Traiter_des_donn-es
Cartographie des supports radioélectriques
Présentation du projet

Ce projet consiste à développer une application interactive de visualisation et d'analyse des supports radioélectriques à l'aide de Python, Dash, Plotly et Pandas.

L'application permet de consulter les données relatives aux supports radioélectriques, de visualiser leur répartition géographique sur une carte interactive et d'obtenir plusieurs indicateurs statistiques concernant les propriétaires, les exploitants et les départements.

Fonctionnalités

L'application propose quatre principales fonctionnalités :

1. Tableau de données

Un tableau interactif réalisé avec Dash AG Grid permet de consulter l'ensemble des données fusionnées.

Les informations disponibles comprennent notamment :

L'identifiant de la station.
La date de mise en service.
La hauteur du support.
Les coordonnées géographiques (latitude et longitude).
Le code postal et le lieu d'implantation.
Le propriétaire du support.
La nature du support.
Le type d'antenne.
L'exploitant.
2. Statistiques sur les propriétaires

Un graphique en barres présente le Top 10 des propriétaires possédant le plus grand nombre de supports radioélectriques.

3. Statistiques sur les exploitants

Un graphique en barres présente le Top 10 des exploitants ayant le plus grand nombre de supports référencés.

4. Répartition géographique

Une carte interactive réalisée avec Plotly permet de visualiser la localisation des supports radioélectriques.

Les fonctionnalités de la carte comprennent :

La localisation des supports à partir de leurs coordonnées géographiques.
La représentation de la hauteur des supports par la taille des marqueurs.
Le regroupement automatique des marqueurs pour faciliter la lecture de la carte.
L'affichage d'informations détaillées au survol d'un support :
Date de mise en service.
Hauteur.
Code postal.
Propriétaire.
Type de support.
Type d'antenne.
Exploitant.
5. Statistiques par département

Un graphique en barres présente le Top 10 des départements possédant le plus grand nombre de supports radioélectriques.

Sources de données

Le projet utilise plusieurs fichiers au format TXT, structurés avec un séparateur point-virgule (;).

Données de référence (ref/)
Fichier	Description
sup_type_antenne.txt	Référentiel des types d'antennes
sup_proprietaire.txt	Référentiel des propriétaires
sup_nature.txt	Référentiel des natures de supports
sup_exploitant.txt	Référentiel des exploitants
Données principales (data/)
Fichier	Description
sup_antenne.txt	Informations sur les antennes
sup_station.txt	Informations sur les stations
sup_support.txt	Informations sur les supports radioélectriques
Traitement des données

Les données sont préparées et enrichies à l'aide de la bibliothèque Pandas.

Les principales étapes de traitement sont les suivantes :

Importation des données : lecture des fichiers TXT avec Pandas.
Sélection des colonnes : conservation des informations nécessaires à l'analyse.
Fusion des données : rapprochement des différentes tables à l'aide de jointures externes gauches (left join).
Conversion des coordonnées géographiques : transformation des coordonnées exprimées en degrés, minutes et secondes (DMS) en coordonnées décimales.
Nettoyage des données :
Conversion des coordonnées en valeurs numériques.
Remplacement des valeurs manquantes par « Inconnu » pour les champs textuels.
Conversion de la hauteur en valeur numérique.
Remplacement des hauteurs manquantes ou inférieures à 1 mètre par une valeur de 1 mètre.
Extraction du département : récupération des deux premiers caractères du code postal.
Préparation des visualisations : calcul des classements et création des graphiques statistiques.
Technologies utilisées
Technologie	Utilisation
Python	Langage de programmation
Pandas	Importation, nettoyage et fusion des données
Dash	Création de l'application web interactive
Dash AG Grid	Affichage du tableau de données
Plotly Express	Création des graphiques et de la carte interactive
Installation
Prérequis
Python 3.9 ou supérieur.
pip (gestionnaire de paquets Python).
1. Cloner ou télécharger le projet

Récupérer les fichiers du projet sur votre ordinateur.

2. Installer les dépendances

Dans un terminal, exécuter la commande suivante :

bash
pip install dash dash-ag-grid pandas plotly

3. Vérifier l'organisation des fichiers

L'arborescence attendue est la suivante :

text
projet/
│
├── app.py
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
└── README.md

4. Lancer l'application

Depuis le répertoire principal du projet, exécuter :

bash
python app.py


L'application Dash sera ensuite accessible depuis un navigateur web à l'adresse :

text
http://127.0.0.1:8050/

Résultat attendu

L'application affiche une interface composée de :

Un tableau récapitulatif des supports radioélectriques.
Un graphique présentant les 10 principaux propriétaires.
Un graphique présentant les 10 principaux exploitants.
Un graphique présentant les 10 départements les plus représentés.
Une carte interactive permettant d'explorer la répartition géographique des supports.
Améliorations possibles

Plusieurs évolutions peuvent être envisagées :

Ajouter des filtres interactifs par département, propriétaire, exploitant ou type de support.
Permettre la recherche d'un support dans le tableau.
Ajouter des indicateurs statistiques globaux (nombre total de supports, hauteur moyenne, etc.).
Ajouter des filtres temporels sur les dates de mise en service.
Améliorer les performances de chargement pour les grands volumes de données.
Ajouter des possibilités d'exportation des données filtrées.
Auteur : AGABA James

Projet de cartographie et d'analyse des supports radioélectriques.
