import time


class MoteurExercice:
    def __init__(self, texte):
        self.texte = texte
        self.index = 0
        self.fautes = 0
        self.start_time = None
        self.end_time = None

    def traiter_entree(self, char):
        if self.est_termine:
            return

        if self.start_time is None:
            self.start_time = time.monotonic()

        attendu = self.caractere_attendu
        if attendu is None:
            return

        if char == attendu:
            self.index += 1
            if self.index >= len(self.texte):
                self.end_time = time.monotonic()
        else:
            self.fautes += 1

    @property
    def caractere_attendu(self):
        if self.index >= len(self.texte):
            return None
        return self.texte[self.index]

    @property
    def est_termine(self):
        return self.index >= len(self.texte)

    @property
    def temps_ecoule(self):
        if self.start_time is None:
            return 0
        if self.end_time is not None:
            return self.end_time - self.start_time
        return time.monotonic() - self.start_time
