import random
import re
import string


def charger_texte_fichier(path):
    with open(path, "r", encoding="utf-8") as f:
        texte = f.read()
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def generer_texte_aleatoire(n=200, alphabet=string.ascii_lowercase):
    lettres = [random.choice(alphabet) for _ in range(n)]
    return " ".join(lettres)
