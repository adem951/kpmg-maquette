# GUIDE DE DÉMARRAGE RAPIDE

## 🚀 Démarrage en 5 minutes

### 1. Installation des dépendances

```bash
# Frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### 2. Configuration minimale

```bash
# Backend: Créer backend/.env
TAVILY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Frontend: Créer .env
REACT_APP_API_URL=http://localhost:8000
```

### 3. Lancement

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
npm start
```

### 4. Accès
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs API: http://localhost:8000/docs

---

## ✨ Fonctionnalités Implémentées

### ✅ Backend Python (FastAPI)
- API REST avec CORS configuré
- Service Tavily (recherche web 2 modes)
- Service LLM (génération analyses)
- Service données (abstraction BDD)
- Filtrage sources fiables
- Scoring de fiabilité

### ✅ Frontend React
- Chatbot interactif
- Modes recherche (Général/Données)
- Graphiques dynamiques (Chart.js)
- Affichage des sources
- Gestion erreurs et chargement
- Interface responsive

### ✅ Intégration RAG
- Recherche contexte web
- Enrichissement LLM
- Sources traçables
- Format standardisé

---

## 📊 Types de Graphiques

1. **Taille du marché** - Barres
2. **Parts de marché** - Circulaire
3. **Croissance régionale** - Barres multiples
4. **Évolution prix** - Lignes

Tous les graphiques affichent les sources dans les tooltips.

---

## 🔑 Clés API Requises

### Tavily (Recherche Web)
- Site: https://tavily.com
- Gratuit?: À vérifier selon usage
- Fonction: Recherche structurée web

### OpenAI (LLM)
- Site: https://platform.openai.com
- Gratuit?: Crédits initiaux puis payant
- Alternatives: Hugging Face, Ollama (local)

**Mode Mock**: Sans clés API, le système utilise des données de démonstration.

---

## 🗄️ Base de Données (Optionnel)

Prêt pour:
- PostgreSQL (relationnel)
- MongoDB (NoSQL)

Configuration dans `backend/.env`:
```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

Les méthodes sont déjà préparées dans `data_service.py`.

---

## 📱 Utilisation

1. **Poser une question** dans le chatbot
2. **Choisir le mode**: Général ou Données
3. **Attendre l'analyse** (quelques secondes)
4. **Consulter les résultats**:
   - Analyse qualitative avec sources
   - Graphiques quantitatifs interactifs
   - Sources fiables listées

---

## 🛠️ Développement

### Ajouter une source fiable

Dans `backend/services/tavily_service.py`:
```python
self.trusted_domains = {
    "market_report": [
        "nouveausite.com",  # Ajouter ici
        ...
    ]
}
```

### Modifier les graphiques

Dans `src/components/QuantitativeAnalysis.js`:
- Personnaliser les options Chart.js
- Ajouter de nouveaux types de graphiques
- Modifier les couleurs et styles

---

## 🔍 Modes de Recherche

### Mode Général 🔍
- Vue d'ensemble
- Tendances secteur
- Acteurs principaux
- Articles et analyses
- **Filtre**: Score ≥ 70

### Mode Données 📊
- Chiffres clés
- Statistiques officielles
- Tailles de marché
- Données quantitatives
- **Filtre**: Score ≥ 80

---

## 💡 Conseils

1. **Développement**: Utilisez le mode mock sans API
2. **Production**: Configurez toutes les clés API
3. **BDD**: Ajoutez quand le volume augmente
4. **Performance**: Utilisez un cache pour Tavily
5. **Sécurité**: Ne commitez jamais les fichiers `.env`

---

Pour plus de détails, consultez [README_INTEGRATION.md](README_INTEGRATION.md)
