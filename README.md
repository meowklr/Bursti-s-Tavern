# Bursti's Tavern

Bursti's Tavern est un jeu d'arcade 2D développé en Python avec Pygame CE, dans le cadre d'un projet de 2e année d'études. Le joueur incarne un serveur qui doit récupérer des aliments et les lancer aux clients assis dans la taverne avant que cinq tables soient occupées en même temps. Projet réalisé dans le cadre d'un devoir en 2ème année d'études, assisté par IA.

## Fonctionnement

Les clients arrivent par les entrées de la taverne et se dirigent vers une table libre. Une fois assis, leur commande (steak, salade ou eau) s'affiche au-dessus d'eux. Le joueur doit ramasser l'aliment correspondant sur la carte et le lancer dans leur direction. Chaque client servi rapporte 100 points et quitte la salle.

Les projectiles rebondissent sur les murs jusqu'à six fois. La partie s'arrête dès que cinq clients sont assis simultanément. En fin de partie, le joueur peut saisir un pseudo (12 caractères alphanumériques maximum) pour enregistrer son score dans [`data/leaderboard.json`](data/leaderboard.json).

## Stack technique

Le projet repose sur Python 3 et Pygame CE (`pygame-ce`), sans autre dépendance externe. La gestion des fichiers, du JSON, des chemins et du pathfinding utilise uniquement la bibliothèque standard Python (`pathlib`, `json`, `random`, `collections`).

## Prérequis et installation

Il faut disposer de Python 3 et de Pygame CE. Depuis la racine du projet :

```bash
python -m pip install -r requirements.txt
```

## Lancer le jeu

```bash
python main.py
```

Les images (sprites et arrière-plan) et les fichiers audio (musique et bruitages) sont inclus dans [`assets/`](assets/).

## Commandes

| Action | Commande |
| --- | --- |
| Se déplacer | `ZQSD` ou flèches directionnelles |
| Viser | Déplacer la souris |
| Lancer un aliment | Clic gauche |
| Démarrer une partie | `Entrée` |
| Mettre en pause / reprendre | `Échap` |
| Recommencer depuis la pause | `R` |
| Recommencer après la fin | `Ctrl + R` |
| Enregistrer son pseudo | Clavier, puis `Entrée` |
| Quitter | Fermer la fenêtre ou `Échap` sur un menu |

## Structure du projet

```text
.
├── main.py                  # Point d'entrée qui initialise Pygame et lance Game
├── requirements.txt         # Dépendances Python du projet
├── LICENSE                  # Licence MIT
├── game/
│   ├── assets.py            # Chargement des images, sons et musique
│   ├── client.py            # États, déplacements et commandes des clients
│   ├── collisions.py        # Vérification des collisions joueur et projectiles
│   ├── constants.py         # Constantes de gameplay (vitesses, rayons, aliments)
│   ├── game.py              # Boucle principale, événements et logique de partie
│   ├── leaderboard.py       # Lecture et écriture des meilleurs scores
│   ├── map.py               # Grille de la taverne et calcul de chemin (BFS)
│   ├── map_render.py        # Affichage de la grille et des aliments au sol
│   ├── player.py            # Déplacements, ramassage et tir du joueur
│   └── projectile.py        # Trajectoire et rebonds des aliments lancés
├── ui/
│   └── hud.py               # Affichage du score, du HUD, de la pause et des menus
├── assets/
│   ├── images/              # Sprites du joueur, du gobelin, des aliments et décor
│   └── sounds/              # Musique d'ambiance et effets sonores
└── data/
    └── leaderboard.json     # Sauvegarde locale des meilleurs scores
```
