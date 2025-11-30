# Script de déploiement sur GitHub Pages

## Instructions de déploiement

### 1. Initialiser Git et connecter au repository
```powershell
git init
git add .
git commit -m "Initial commit - KPMG Market Analysis App"
git branch -M main
git remote add origin https://github.com/adem951/kpmg-maquette.git
git push -u origin main
```

### 2. Installer gh-pages
```powershell
npm install
```

### 3. Déployer sur GitHub Pages
```powershell
npm run deploy
```

### 4. Activer GitHub Pages (si ce n'est pas déjà fait)
1. Allez sur https://github.com/adem951/kpmg-maquette/settings/pages
2. Sélectionnez la branche `gh-pages` comme source
3. Cliquez sur "Save"

### 5. Accéder à votre application
Votre application sera disponible à l'adresse :
**https://adem951.github.io/kpmg-maquette/**

## Commandes utiles

- `npm start` : Lance l'application en local
- `npm run build` : Compile l'application
- `npm run deploy` : Déploie sur GitHub Pages

## Mise à jour de l'application

Pour mettre à jour l'application après des modifications :

```powershell
git add .
git commit -m "Description de vos modifications"
git push
npm run deploy
```

## Note importante

Le déploiement sur GitHub Pages est gratuit et votre application sera accessible publiquement via le lien fourni.
