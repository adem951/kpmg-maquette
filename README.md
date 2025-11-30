# Market Analysis Platform - KPMG

Application web React statique pour l'analyse de marché avec assistant IA simulé.

## 🚀 Fonctionnalités

- **Chat interactif** : Interface conversationnelle pour soumettre des demandes d'analyse
- **Analyse qualitative** : Résultats textuels détaillés avec recommandations stratégiques
- **Analyse quantitative** : Visualisations graphiques (graphiques en barres, camemberts, courbes)
- **Données pré-enregistrées** : Simule les réponses IA avec des exemples concrets
- **Interface moderne** : Design professionnel aux couleurs KPMG

## 📊 Exemples d'analyses disponibles

1. **Marché des véhicules électriques**
   - Évolution de la taille du marché
   - Parts de marché des acteurs principaux
   - Distribution régionale et croissance
   - Tendances et recommandations

2. **E-commerce en France**
   - Contexte du marché français
   - Comportements consommateurs
   - Secteurs porteurs
   - Innovations technologiques

3. **Analyse générique**
   - Template par défaut pour autres secteurs

## 🛠️ Installation

### Prérequis

- Node.js (version 14 ou supérieure)
- npm ou yarn

### Étapes d'installation

1. Installer les dépendances :
```bash
npm install
```

2. Lancer l'application en mode développement :
```bash
npm start
```

3. Ouvrir [http://localhost:3000](http://localhost:3000) dans votre navigateur

## 📦 Structure du projet

```
src/
├── components/
│   ├── ChatBox.js              # Composant de chat interactif
│   ├── ChatBox.css
│   ├── QualitativeAnalysis.js  # Affichage analyse qualitative
│   ├── QualitativeAnalysis.css
│   ├── QuantitativeAnalysis.js # Graphiques et visualisations
│   └── QuantitativeAnalysis.css
├── mockData.js                 # Données fictives simulant l'IA
├── App.js                      # Composant principal
├── App.css
├── index.js
└── index.css
```

## 🎨 Technologies utilisées

- **React** : Framework JavaScript
- **Chart.js** : Bibliothèque de graphiques
- **react-chartjs-2** : Wrapper React pour Chart.js
- **CSS3** : Animations et design moderne

## 💡 Utilisation

1. Tapez votre demande d'analyse dans le chat
2. Utilisez les suggestions rapides pour des exemples prédéfinis
3. L'assistant IA simule le traitement de la demande
4. Les résultats s'affichent avec :
   - Une analyse qualitative détaillée
   - Des graphiques quantitatifs interactifs
   - Des recommandations stratégiques

## 🔧 Personnalisation

Pour ajouter de nouvelles analyses, modifiez le fichier `src/mockData.js` en ajoutant de nouveaux objets dans `mockAnalyses`.

## 📝 Scripts disponibles

- `npm start` : Lance l'application en mode développement
- `npm run build` : Compile l'application pour la production
- `npm test` : Lance les tests
- `npm run eject` : Éjecte la configuration (irréversible)

## 🌐 Build pour production

```bash
npm run build
```

Le dossier `build` contient les fichiers optimisés prêts pour le déploiement.

## 📄 Licence

Ce projet est une maquette de démonstration créée pour KPMG.

## 👥 Support

Pour toute question ou suggestion, contactez l'équipe de développement.
