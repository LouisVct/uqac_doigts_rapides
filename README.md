# uqaq_typing_learn

Application d'entrainement a la frappe au clavier avec rendu visuel d'un clavier, exercices progressifs et score final.

## Fonctionnalites

- Hub de configuration au lancement (mode + niveau d'aide).
- Affichage en plein ecran avec zone de texte + clavier visuel.
- 3 modes d'exercice:
  - texte complet depuis un fichier,
  - mots aleatoires,
  - lettres aleatoires.
- 3 niveaux d'aide (dont un niveau avec surbrillance des touches a utiliser en cas d'erreur/inactivite).
- Score final affiche avec nombre de fautes et temps total.
- Sons d'erreur et de fin (si le systeme audio est disponible).

## Prerequis

- Python 3.9+
- `pip`

## Installation et lancement

Depuis la racine du projet:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\main.py
```

### Lancement direct sans activation du venv

```bash
./.venv/bin/python main.py
```

ou sous Windows:

```powershell
.\.venv\Scripts\python.exe .\main.py
```

## Utilisation

### Ecran de configuration

- `Haut/Bas` ou `W/S`: changer de section.
- `Gauche/Droite` ou `A/D`: changer d'option.
- `Entree` ou `Espace`: lancer la session.
- `Esc`: quitter.

### Pendant l'exercice

- Tape le caractere attendu.
- En mode aide niveau 1, les touches sont surlignees apres erreur ou apres quelques secondes d'inactivite.
- `Esc`: quitter l'application.

### Fin d'exercice

- Le score s'affiche (`fautes`, `temps`).
- `Entree` ou `Espace`: retour au hub.

## Modes disponibles

- `Texte du fichier`: charge `assets/contents/texte.txt`.
- `Mots aleatoires`: enchaine des mots uniques issus de `assets/contents/mots.txt` (30 mots par session).
- `Lettres aleatoires`: enchaine les lettres de l'alphabet en ordre melange.

Notes importantes:

- Les modes aleatoires normalisent la saisie en minuscules.
- Pour le mode mots, seuls les mots alphabetiques ASCII sont retenus (pas d'accents/ponctuation dans la liste utile).

## Personnalisation

- Modifier `assets/contents/texte.txt` pour changer le texte d'entrainement.
- Modifier `assets/contents/mots.txt` pour la base de mots aleatoires.
- Modifier `clavier.json` pour adapter la disposition du clavier et les compositions speciales.
- Remplacer les sons dans `assets/songs/` si besoin.

## Structure rapide du projet

```text
.
|-- main.py
|-- app/
|   |-- configuration_screen.py
|   |-- session_controller.py
|   `-- constants.py
|-- screenText.py
|-- screenKeyboard.py
|-- clavier.py
|-- moteur.py
|-- modes.py
|-- clavier.json
`-- assets/
    |-- contents/
    |-- fonts/
    `-- songs/
```

## Depannage

- Pas de son: l'application continue de fonctionner meme sans initialisation audio.
- Erreur de fichier ou de configuration: un ecran bloquant affiche le detail et permet de revenir au hub.
- Erreur "pas assez de mots valides": verifier le contenu de `assets/contents/mots.txt`.

## Credits audio

- `assets/songs/aplause.wav`: https://lasonotheque.org/applaudissements-25-50-pers-1-s0812.html
- `assets/songs/error.wav`: https://lasonotheque.org/docteur-maboul-4-s1685.html
