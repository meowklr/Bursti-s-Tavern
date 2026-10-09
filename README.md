# Bursti's Tavern

Bursti's Tavern est un petit jeu de taverne développé en Python avec
Pygame. Le joueur doit récupérer les aliments, servir les clients assis en
lançant leur commande, et éviter de laisser cinq tables occupées.

## Fonctionnement

Les clients arrivent par les entrées de la taverne et rejoignent une table
libre. Leur commande est affichée au-dessus d'eux lorsqu'ils sont assis.
Apportez le bon aliment au client pour le faire partir et gagner 100 points.
La partie se termine lorsque cinq clients sont assis en même temps.

Les meilleurs scores sont enregistrés dans
[`data/leaderboard.json`](data/leaderboard.json).

## Installation

Prérequis :

- Python 3 ;
- Pygame.

Depuis le dossier du projet, installez Pygame :

```bash
python -m pip install pygame
```

## Lancer le jeu

```bash
python main.py
```

Les images et les sons nécessaires sont déjà présents dans le dossier
[`assets/`](assets/).

## Commandes

| Action | Commande |
| --- | --- |
| Se déplacer | `ZQSD` ou les flèches directionnelles |
| Viser | Déplacer la souris |
| Lancer un aliment | Clic gauche |
| Démarrer une partie | `Entrée` |
| Mettre en pause / reprendre | `Échap` |
| Recommencer depuis la pause | `R` |
| Recommencer après la fin | `Ctrl + R` |
| Saisir le pseudo après la fin | Clavier, puis `Entrée` pour sauvegarder |
| Quitter | Fermer la fenêtre ou `Échap` depuis un écran de menu |

## Organisation du projet

```text
.
├── main.py                  # Point d'entrée du jeu
├── game/                    # Logique, carte, collisions et entités
├── ui/                      # Affichage du HUD et des menus
├── assets/
│   ├── images/              # Sprites et arrière-plan
│   └── sounds/              # Effets sonores et musique
└── data/
    └── leaderboard.json     # Meilleurs scores
```
