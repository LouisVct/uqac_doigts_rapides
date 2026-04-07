import random
import re
import string


CARACTERES_INTERDITS = set(",?;.:/ éàèùâêîôûëïüÿ")


def charger_texte_fichier(path):
    with open(path, "r", encoding="utf-8") as f:
        texte = f.read()
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def _mot_est_valide(mot):
    if not mot:
        return False
    mot = mot.lower()
    if any(char in CARACTERES_INTERDITS for char in mot):
        return False
    return mot.isalpha() and mot.isascii()


def extraire_mots_valides(texte):
    mots = re.findall(r"\S+", texte)
    return [mot for mot in mots if _mot_est_valide(mot)]


def generer_mots_aleatoires(path, n=40):
    texte = charger_texte_fichier(path)
    mots_valides = extraire_mots_valides(texte)
    if not mots_valides:
        raise ValueError("Aucun mot valide trouve dans le texte source.")
    return " ".join(random.choice(mots_valides).lower() for _ in range(n))


def generer_mot_aleatoire(path):
    return generer_mots_aleatoires(path, 1)


class FournisseurMotsUniques:
    def __init__(self, path, limite=None):
        texte = charger_texte_fichier(path)
        mots = [mot.lower() for mot in extraire_mots_valides(texte)]

        # On dedoublonne tout en conservant l'ordre du texte source.
        mots_uniques = list(dict.fromkeys(mots))
        if not mots_uniques:
            raise ValueError("Aucun mot valide trouve dans le texte source.")

        if limite is not None:
            if limite <= 0:
                raise ValueError("La limite de mots doit etre superieure a 0.")
            if len(mots_uniques) < limite:
                raise ValueError(
                    f"Pas assez de mots valides: {len(mots_uniques)} disponibles pour une limite de {limite}."
                )
            mots_uniques = mots_uniques[:limite]

        self._restants = mots_uniques[:]
        random.shuffle(self._restants)

    def prochain(self):
        if not self._restants:
            raise StopIteration("Plus de mots disponibles pour cette session.")
        return self._restants.pop()


class FournisseurLettresUniques:
    def __init__(self, alphabet=string.ascii_lowercase):
        lettres = [
            char
            for char in alphabet
            if char not in CARACTERES_INTERDITS and not char.isspace()
        ]
        # On supprime les doublons en conservant l'ordre.
        lettres_uniques = list(dict.fromkeys(lettres))
        if not lettres_uniques:
            raise ValueError("Aucune lettre autorisee disponible.")

        self._restantes = lettres_uniques[:]
        random.shuffle(self._restantes)

    def prochain(self):
        if not self._restantes:
            raise StopIteration("Plus de lettres disponibles pour cette session.")
        return self._restantes.pop()


def generer_lettres_aleatoires(n=200, alphabet=string.ascii_lowercase):
    alphabet_filtre = [
        char
        for char in alphabet
        if char not in CARACTERES_INTERDITS and not char.isspace()
    ]
    if not alphabet_filtre:
        raise ValueError("L'alphabet ne contient aucun caractere autorise.")
    return "".join(random.choice(alphabet_filtre) for _ in range(n))


def generer_lettre_aleatoire(alphabet=string.ascii_lowercase):
    return generer_lettres_aleatoires(1, alphabet)
