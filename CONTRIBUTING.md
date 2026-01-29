# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 

## Permissions du Repository

Ce repository est configuré de la manière suivante :
- 👁️ **Visibilité publique** : Tout le monde peut voir le code
- 🔒 **Écriture limitée** : Seuls les collaborateurs peuvent push directement
- 🤝 **Contributions ouvertes** : Tout le monde peut contribuer via Pull Requests

## Pour les Non-Collaborateurs

Si vous n'êtes pas collaborateur du repository, vous pouvez toujours contribuer :

### 1. Fork le Repository
Cliquez sur le bouton "Fork" en haut à droite de la page GitHub

### 2. Cloner votre Fork
```bash
git clone https://github.com/VOTRE-USERNAME/uqac_doigts_rapides.git
cd uqac_doigts_rapides
```

### 3. Configurer l'environnement
```bash
python3 -m venv virtualEnvDoigtsRapides
source ./virtualEnvDoigtsRapides/bin/activate  # Linux/Mac
# OU
.\virtualEnvDoigtsRapides\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4. Créer une Branche
```bash
git checkout -b ma-nouvelle-fonctionnalite
```

### 5. Faire vos Modifications
Effectuez vos modifications dans le code

### 6. Commit et Push
```bash
git add .
git commit -m "Description de mes modifications"
git push origin ma-nouvelle-fonctionnalite
```

### 7. Créer une Pull Request
Allez sur GitHub et créez une Pull Request depuis votre fork vers le repository principal

## Pour les Collaborateurs

Si vous êtes collaborateur du repository :

### 1. Cloner Directement
```bash
git clone https://github.com/LouisVct/uqac_doigts_rapides.git
cd uqac_doigts_rapides
```

### 2. Créer une Branche
```bash
git checkout -b ma-nouvelle-fonctionnalite
```

### 3. Développer et Push
```bash
git add .
git commit -m "Description de mes modifications"
git push origin ma-nouvelle-fonctionnalite
```

### 4. Créer une Pull Request
Même en tant que collaborateur, il est recommandé de créer des Pull Requests pour permettre la revue de code

## Bonnes Pratiques

- ✅ Utilisez des messages de commit descriptifs
- ✅ Testez votre code avant de push
- ✅ Créez des Pull Requests pour toutes les modifications importantes
- ✅ Documentez les nouvelles fonctionnalités
- ❌ Ne push jamais directement sur `main`/`master`
- ❌ Ne commitez jamais de secrets ou credentials

## Questions ?

Si vous avez des questions sur le processus de contribution, n'hésitez pas à créer une Issue !
