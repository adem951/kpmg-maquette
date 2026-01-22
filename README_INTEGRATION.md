# KPMG Market Analysis Platform - Guide d'Installation et d'Utilisation

## 📋 Vue d'ensemble

Cette plateforme d'analyse de marché intègre :
- ✅ **Frontend React** avec graphiques dynamiques (Chart.js)
- ✅ **Backend Python FastAPI** avec orchestration LLM
- ✅ **Recherche web Tavily** (modes général et données)
- ✅ **Abstraction BDD** prête pour PostgreSQL/MongoDB
- ✅ **Sources fiables** avec score de fiabilité
- ✅ **Architecture RAG** pour analyses enrichies

---

## 🚀 Installation

### Prérequis
- **Node.js** (v16 ou supérieur)
- **Python** (3.9 ou supérieur)
- **pip** et **npm**

### 1. Installation du Frontend

```bash
# Depuis la racine du projet
npm install
```

### 2. Installation du Backend

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel Python (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Configuration du Backend

Créer un fichier `.env` dans le dossier `backend/` :

```bash
# Copier le fichier d'exemple
cd backend
cp .env.example .env
```

Éditer le fichier `.env` avec vos clés API :

```env
# API Keys
TAVILY_API_KEY=votre_clé_tavily_ici
OPENAI_API_KEY=votre_clé_openai_ici

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Database Configuration (optionnel - à configurer plus tard)
# DATABASE_TYPE=postgresql
# DATABASE_URL=postgresql://user:password@localhost:5432/market_analysis
```

### 2. Configuration du Frontend

Créer un fichier `.env` à la racine du projet :

```bash
# Copier le fichier d'exemple
cp .env.example .env
```

Contenu du fichier `.env` :

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🏃 Démarrage

### 1. Démarrer le Backend

```bash
# Depuis le dossier backend/
cd backend
python main.py
```

Le backend sera accessible sur : **http://localhost:8000**

Vérifier l'état : **http://localhost:8000/health**

### 2. Démarrer le Frontend

```bash
# Depuis la racine du projet
npm start
```

Le frontend sera accessible sur : **http://localhost:3000**

---

## 📡 API Endpoints

### Backend FastAPI

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | État de l'API |
| `/health` | GET | Vérification santé |
| `/api/search/general` | POST | Recherche générale (contexte, tendances) |
| `/api/search/data` | POST | Recherche de données quantitatives |
| `/api/analysis` | POST | Génération d'analyse complète |
| `/api/market-data` | GET | Récupération données marché |
| `/api/market-data` | POST | Sauvegarde données marché |

### Exemple d'appel API

```javascript
// Génération d'une analyse
const response = await fetch('http://localhost:8000/api/analysis', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "Marché des véhicules électriques",
    include_web_search: true
  })
});

const data = await response.json();
```

---

## 🎯 Fonctionnalités Principales

### 1. Recherche Tavily (2 modes)

#### Mode Général
- Contexte marché
- Tendances
- Acteurs principaux
- Articles et analyses

#### Mode Données
- Chiffres clés
- Statistiques
- Tailles de marché
- Données quantitatives

### 2. Filtrage des Sources Fiables

Le système attribue automatiquement un score de fiabilité :
- **95/100** : Sources gouvernementales (.gov, .gouv)
- **90/100** : Rapports de cabinets (KPMG, McKinsey, Gartner)
- **85/100** : Médias économiques (Les Échos, Financial Times)
- **60/100** : Autres sources

### 3. Graphiques Dynamiques

- **Taille du marché** : Graphique en barres
- **Parts de marché** : Graphique circulaire
- **Croissance régionale** : Barres multiples
- **Évolution des prix** : Graphique linéaire

Chaque graphique affiche les sources dans les tooltips.

### 4. Abstraction BDD (Prête pour intégration)

Le service `data_service.py` est préparé pour :
- **PostgreSQL** : Bases relationnelles
- **MongoDB** : Bases NoSQL

```python
# À configurer dans .env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/market_analysis
```

---

## 📦 Structure du Projet

```
Kpmg analyse de marché/
├── backend/
│   ├── main.py                    # API FastAPI principale
│   ├── requirements.txt           # Dépendances Python
│   ├── .env.example               # Configuration exemple
│   └── services/
│       ├── tavily_service.py      # Service Tavily (recherche web)
│       ├── llm_service.py         # Service LLM (génération)
│       └── data_service.py        # Service données (BDD)
├── src/
│   ├── App.js                     # Composant principal
│   ├── App.css                    # Styles globaux
│   ├── services/
│   │   └── apiService.js          # Service API frontend
│   └── components/
│       ├── ChatBox.js             # Chatbot avec modes recherche
│       ├── QualitativeAnalysis.js # Analyse qualitative + sources
│       └── QuantitativeAnalysis.js# Graphiques + sources
├── package.json
├── .env.example
└── README_INTEGRATION.md
```

---

## 🔧 Configuration Avancée

### Ajout d'une Base de Données

#### PostgreSQL

1. Installer PostgreSQL
2. Créer une base de données :
```sql
CREATE DATABASE market_analysis;
```

3. Configurer dans `.env` :
```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/market_analysis
```

4. Dans `data_service.py`, décommenter les méthodes SQL

#### MongoDB

1. Installer MongoDB
2. Configurer dans `.env` :
```env
DATABASE_TYPE=mongodb
MONGODB_URL=mongodb://localhost:27017/market_analysis
```

3. Dans `data_service.py`, décommenter les méthodes MongoDB

---

## 🔑 Obtenir les Clés API

### Tavily API
1. Visiter : https://tavily.com
2. Créer un compte
3. Générer une clé API
4. Ajouter dans `backend/.env`

**Note** : Vérifier si Tavily nécessite un abonnement payant pour votre usage.

### OpenAI API (pour le LLM)
1. Visiter : https://platform.openai.com
2. Créer un compte
3. Générer une clé API
4. Ajouter dans `backend/.env`

**Alternatives gratuites** :
- Hugging Face (modèles open-source)
- Ollama (local)

---

## 🧪 Tests

### Tester le Backend

```bash
# Health check
curl http://localhost:8000/health

# Test recherche générale
curl -X POST http://localhost:8000/api/search/general \
  -H "Content-Type: application/json" \
  -d '{"query": "marché des véhicules électriques", "max_results": 5}'

# Test analyse complète
curl -X POST http://localhost:8000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{"query": "e-commerce en France", "include_web_search": true}'
```

### Tester le Frontend

1. Ouvrir http://localhost:3000
2. Taper une requête dans le chatbot
3. Vérifier les modes "Général" et "Données"
4. Observer les graphiques et les sources

---

## 🐛 Dépannage

### Backend ne démarre pas
- Vérifier que Python 3.9+ est installé
- Vérifier que l'environnement virtuel est activé
- Vérifier le fichier `.env`

### Frontend ne se connecte pas au Backend
- Vérifier que le backend tourne sur le port 8000
- Vérifier le fichier `.env` du frontend
- Vérifier CORS dans `main.py`

### Pas de résultats Tavily
- Vérifier la clé API Tavily dans `.env`
- Le système utilise des données mock si Tavily n'est pas configuré

---

## 📚 Prochaines Étapes

### Fonctionnalités à ajouter
- ✅ Connexion BDD réelle (PostgreSQL/MongoDB)
- ✅ Authentification utilisateurs
- ✅ Sauvegarde des analyses
- ✅ Téléchargement PDF des rapports
- ✅ Comparaison de marchés
- ✅ Alertes et notifications

### Optimisations
- Cache des résultats Tavily
- Rate limiting API
- Compression des réponses
- Tests unitaires et d'intégration

---

## 📞 Support

Pour toute question ou problème :
- Vérifier la documentation API : http://localhost:8000/docs
- Consulter les logs du backend
- Vérifier la console du navigateur (F12)

---

## 📄 Licence

Propriété de KPMG - Tous droits réservés.
