# CONFIGURATION DES VARIABLES D'ENVIRONNEMENT SYSTÈME

## 🔐 Utilisation de variables d'environnement au lieu de .env

Le backend utilise maintenant `os.getenv()` pour lire les clés API directement depuis les variables d'environnement système.

---

## ⚙️ Configuration sous Windows

### Option 1: SETX (Recommandé - Permanent)

**La méthode la plus simple sous Windows** :

```cmd
# Ouvrir une invite de commande (CMD) ou PowerShell
setx TAVILY_API_KEY "votre_clé_tavily_ici"
setx OPENAI_API_KEY "votre_clé_openai_ici"

# Fermer et rouvrir le terminal pour que les variables soient chargées
# Puis vérifier :
echo %TAVILY_API_KEY%    (CMD)
echo $env:TAVILY_API_KEY  (PowerShell)
```

**Avantage** : Simple, permanent, standard Windows  
**Important** : Fermer et rouvrir le terminal après setx

---

### Option 2: Variables de session PowerShell (temporaires)

```powershell
# Définir les variables (durée de la session uniquement)
$env:TAVILY_API_KEY = "votre_clé_tavily_ici"
$env:OPENAI_API_KEY = "votre_clé_openai_ici"

# Vérifier
echo $env:TAVILY_API_KEY
echo $env:OPENAI_API_KEY

# Lancer le backend dans la même session
cd "c:\Users\debba\OneDrive\Documents\Kpmg analyse de marché\backend"
.\env_market\Scripts\Activate.ps1
python main.py
```

**Avantage** : Les clés ne persistent pas après fermeture du terminal  
**Inconvénient** : À refaire à chaque nouvelle session

---

### Option 3: Variables CMD (temporaires)

```cmd
# Définir les variables (durée de la session uniquement)
set TAVILY_API_KEY=votre_clé_tavily_ici
set OPENAI_API_KEY=votre_clé_openai_ici

# Vérifier
echo %TAVILY_API_KEY%
echo %OPENAI_API_KEY%
```

---

### Option 4: Interface graphique Windows

1. Rechercher "Variables d'environnement" dans Windows
2. Cliquer sur "Modifier les variables d'environnement système"
3. Cliquer sur "Variables d'environnement..."
4. Dans "Variables utilisateur", cliquer "Nouvelle..."
5. Ajouter :
   - Nom : `TAVILY_API_KEY`
   - Valeur : `votre_clé_tavily`
6. Répéter pour `OPENAI_API_KEY`
7. Redémarrer le terminal/VSCode

---

## 🔍 Vérification

Après avoir défini les variables, vérifiez-les avant de lancer le backend :

```cmd
# CMD
echo %TAVILY_API_KEY%
echo %OPENAI_API_KEY%
```

```powershell
# PowerShell
echo $env:TAVILY_API_KEY
echo $env:OPENAI_API_KEY
```

**Important après setx** : Fermez et rouvrez le terminal pour que les variables soient chargées !

---

## 🚀 Démarrage du backend

```powershell
cd "c:\Users\debba\OneDrive\Documents\Kpmg analyse de marché\backend"
.\env_market\Scripts\Activate.ps1
python main.py
```

Le backend affichera un message si les clés ne sont pas trouvées :
- `⚠️ TAVILY_API_KEY non définie - Mode mock activé`
- `cmd
# Supprimer définitivement avec setx (définir à vide)
setx TAVILY_API_KEY ""
setx OPENAI_API_KEY ""
```

```powershell
# Supprimer de la session PowerShell
Remove-Item Env:\TAVILY_API_KEY
Remove-Item Env:\OPENAI_API_KEY

# Ou définitivement
```powershell
# Supprimer de la session
Remove-Item Env:\TAVILY_API_KEY
Remove-Item Env:\OPENAI_API_KEY

# Supprimer définitivement (utilisateur)
[System.Environment]::SetEnvironmentVariable("TAVILY_API_KEY", $null, "User")
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $null, "User")
```

---

## 🔒 Sécurité

### ✅ Avantages de cette approche
- Les clés ne sont **jamais stockées en clair** dans les fichiers du projet
- Pas de risque d'exposition via Git (pas de `.env`)
- Les clés sont protégées par les permissions du système d'exploitation

### ⚠️ Bonnes pratiques
- Ne partagez jamais vos clés API
- Utilisez des clés différentes pour dev/prod
- Révoquéz les clés si elles sont compromises
- Utilisez un gestionnaire de secrets en production (Azure Key Vault, AWS Secrets Manager)

---

## 📝 Alternative : Script de démarrage

Créez un fichier `start_backend.ps1` pour automatiser :

```powershell
# start_backend.ps1
$env:TAVILY_API_KEY = "votre_clé_tavily"
$env:OPENAI_API_KEY = "votre_clé_openai"

cd "c:\Users\debba\OneDrive\Documents\Kpmg analyse de marché\backend"
.\env_market\Scripts\Activate.ps1
python main.py
```

⚠️ **Attention** : Ne commitez pas ce fichier sur Git ! Ajoutez-le à `.gitignore`.

---

## 🐧 Bonus : Configuration sous Linux/Mac (Bash)

```bash
# Temporaire (session)
export TAVILY_API_KEY="votre_clé_tavily"
export OPENAI_API_KEY="votre_clé_openai"

# Permanent (ajouter dans ~/.bashrc ou ~/.zshrc)
echo 'export TAVILY_API_KEY="votre_clé_tavily"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="votre_clé_openai"' >> ~/.bashrc
source ~/.bashrc
```
