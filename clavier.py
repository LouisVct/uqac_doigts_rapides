import json


class Touche: 
    def __init__(self, caracteres, hauteur, largeur, frame_color =(0,0,0) , background_color = None, text_color = (0,0,0)):
        self.caracteres = caracteres
        self.hauteur = hauteur
        self.largeur = largeur
        self.frame_color = frame_color
        self.background_color = background_color
        self.text_color = text_color
        self.rect = None
        self.default_frame_color = frame_color
        self.default_background_color = background_color
        self.default_text_color = text_color



class ModeleClavier:
    def __init__(self, chemin_json):
        self.lignes_touches = []       # liste de listes (pour l'affichage ligne par ligne)
        self.dictionnaire_touches = {} # dictionnaire (pour la recherche ultra-rapide)
        
        self.charger_depuis_json(chemin_json)

    def charger_depuis_json(self, chemin):
       
        with open(chemin, 'r', encoding='utf-8') as f: # ouverture du fichier JSON en lecture
            donnees = json.load(f)

        # récupération des données globales
        self.w_reel = donnees["largeur_réel_clavier"]
        self.h_reel = donnees["hauteur_réel_clavier"]
        w_defaut = donnees["largeur_par_default"]
        h_defaut = donnees["hauteur_par_default"]

        # on parcourt les lignes du JSON
        for ligne_json in donnees["touches"]:
            ligne_objets = []
            
            # on parcourt chaque touche dans la ligne
            for t_json in ligne_json:
                
                # récupération des valeurs du JSON et utilisation des valeurs par défaut si nécessaire
                caracs = t_json["caracteres"]
                w = t_json.get("largeur", w_defaut)
                h = t_json.get("hauteur", h_defaut)
                
                # récupération des couleurs, si il n'y en à pas on met des valeurs par défaut
                frame = t_json.get("frame_color", (0, 0, 0))
                bg = t_json.get("background_color", None)
                txt = t_json.get("text_color", (0, 0, 0))
                
                # instanciation d'une touche
                nouvelle_touche = Touche(
                    caracteres=caracs,
                    hauteur=h,          
                    largeur=w,          
                    frame_color=frame,
                    background_color=bg,
                    text_color=txt
                )
                
                # ajout de la touche à la liste (pour pygame)
                ligne_objets.append(nouvelle_touche)
                
                # ajout des tout les caractères de notre touche dans le dictionnaire
                for c in caracs:
                    cle = c.lower()
                    self.dictionnaire_touches[cle] = nouvelle_touche

            # on ajoute la ligne terminée à notre liste globale
            self.lignes_touches.append(ligne_objets)

    def get_touche(self, lettre):
        if not lettre:
            return None
        return self.dictionnaire_touches.get(lettre.lower())

    def get_caracteres_disponibles(self):
        return list(self.dictionnaire_touches.keys())

    def contient_caractere(self, caractere):
        return self.get_touche(caractere) is not None

    def set_touche_background(self, lettre, couleur):
        touche = self.get_touche(lettre)
        if touche is None:
            return False
        touche.background_color = couleur
        return True

    def reset_touche_background(self, lettre):
        touche = self.get_touche(lettre)
        if touche is None:
            return False
        touche.background_color = touche.default_background_color
        return True

