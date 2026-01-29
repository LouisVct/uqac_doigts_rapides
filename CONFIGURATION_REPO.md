# Configuration du Repository GitHub

## Objectif
Ce document explique comment configurer le repository pour que **tout le monde puisse voir le repo mais seuls les collaborateurs peuvent faire des push, merge, etc.**

## Configuration Requise

### 1. Rendre le Repository Public

Pour que tout le monde puisse voir le repository :

1. Allez dans les **Settings** du repository sur GitHub
2. Descendez jusqu'à la section **Danger Zone**
3. Cliquez sur **Change repository visibility**
4. Sélectionnez **Make public**
5. Confirmez en tapant le nom du repository

### 2. Gérer les Permissions des Collaborateurs

GitHub gère automatiquement les permissions pour les repositories publics :

- **Utilisateurs non-collaborateurs** : Peuvent voir le code, cloner le repository, créer des issues et des pull requests
- **Collaborateurs** : Ont les droits d'écriture (push, merge, etc.)

#### Ajouter des Collaborateurs

Pour donner les droits de push/merge à quelqu'un :

1. Allez dans **Settings** → **Collaborators and teams**
2. Cliquez sur **Add people**
3. Recherchez l'utilisateur par son nom d'utilisateur GitHub
4. Sélectionnez le niveau d'accès approprié :
   - **Write** : Peut push et merge (recommandé pour les développeurs)
   - **Maintain** : Peut gérer le repository sans y avoir accès en administration
   - **Admin** : Contrôle total du repository

### 3. Protéger les Branches

Pour éviter les push directs sur la branche principale :

1. Allez dans **Settings** → **Branches**
2. Cliquez sur **Add branch protection rule**
3. Dans "Branch name pattern", entrez `main` ou `master`
4. Cochez les options suivantes :
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals** (nombre de reviews requis)
   - ✅ **Require status checks to pass before merging** (si vous avez des tests)
5. Cliquez sur **Create** ou **Save changes**

## Résumé des Permissions

| Type d'utilisateur | Voir le code | Cloner | Fork | Pull Request | Push | Merge | Paramètres |
|-------------------|--------------|--------|------|--------------|------|-------|------------|
| Public (non connecté) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Connecté (non collaborateur) | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Collaborateur (Write) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Workflow de Contribution

Pour les non-collaborateurs qui souhaitent contribuer :

1. Fork le repository
2. Cloner leur fork
3. Créer une branche pour leurs modifications
4. Faire leurs modifications
5. Push vers leur fork
6. Créer une Pull Request vers le repository principal

Les collaborateurs peuvent créer des Pull Requests directement sans fork.

## Notes Importantes

- ⚠️ Une fois le repository public, tout le monde peut voir le code
- ⚠️ Assurez-vous qu'il n'y a pas de secrets ou credentials dans le code
- ⚠️ Les collaborateurs doivent être des personnes de confiance
- ✅ La protection de branches empêche les modifications accidentelles
- ✅ Les Pull Requests permettent de revoir le code avant merge
