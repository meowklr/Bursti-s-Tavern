import json
from pathlib import Path


class Leaderboard:
    def __init__(self, path): #initialise le leaderboard avec le chemin et les données existantes
        self.path = Path(path)
        self.entries = self.load() 

    def load(self): #charge les données du leaderboard depuis le fichier JSON
        if not self.path.exists(): #si le fichier n'existe pas on le crée
            return []

        try:
            with self.path.open("r", encoding="utf-8") as file:
                entries = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(entries, list):
            return []

        return [
            entry for entry in entries
            if isinstance(entry, dict)
            and isinstance(entry.get("name"), str)
            and isinstance(entry.get("score"), int)
        ]

    def add(self, name, score): #ajoute un nouveau score au leaderboard et le sauvegarde dans le fichier JSON
        self.entries.append({"name": name, "score": score})
        self.entries.sort(key=lambda entry: entry["score"], reverse=True) #trie les scores
        self.entries = self.entries[:10]
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self.entries, file, ensure_ascii=False, indent=2)
