"""
Service LLM pour générer les analyses de marché
Utilise OpenAI GPT pour orchestrer l'analyse avec détection d'intention
"""

from typing import List, Dict, Optional, Tuple
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

# Charger les variables d'environnement depuis le fichier .env du backend
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)


class LLMService:
    """Service pour générer des analyses avec un LLM"""
    
    def __init__(self, api_key: str = None, tavily_service=None, data_service=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Modèle plus récent et économique
        self.tavily_service = tavily_service
        self.data_service = data_service
        
        # Configurer OpenAI client
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Vérifie si le service est configuré"""
        configured = self.api_key is not None and self.api_key != "your_openai_api_key_here" and self.client is not None
        print(f"🔑 LLM configuré: {configured} (api_key: {bool(self.api_key)}, client: {bool(self.client)})")
        return configured
    
    async def detect_market_analysis_intent(self, user_input: str) -> Tuple[bool, str]:
        """
        Détecte si l'entrée utilisateur correspond à une demande d'analyse de marché
        
        Args:
            user_input: La requête de l'utilisateur
        
        Returns:
            Tuple[bool, str]: (est_analyse_marche, explication)
        """
        
        if not self.is_configured():
            # En mode mock, accepter toute demande
            return True, "Mode simulation activé"
        
        try:
            detection_prompt = """Tu es un classificateur d'intentions. Ton rôle est de déterminer si une demande utilisateur concerne une analyse de marché.

Une analyse de marché inclut :
- Étude d'un secteur, d'une industrie ou d'un marché spécifique
- Analyse de la concurrence
- Tendances du marché
- Opportunités commerciales
- Données sur les consommateurs, produits ou services
- Prévisions économiques d'un secteur

Une analyse de marché N'inclut PAS :
- Questions générales non liées au business
- Demandes personnelles
- Conversations informelles
- Questions techniques sans contexte marché

Réponds UNIQUEMENT par un JSON avec ce format exact :
{"is_market_analysis": true/false, "explanation": "explication courte"}

Ne réponds QUE par le JSON, rien d'autre."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": detection_prompt},
                    {"role": "user", "content": f"Demande à classifier : {user_input}"}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            return result.get("is_market_analysis", False), result.get("explanation", "")
            
        except Exception as e:
            print(f"Erreur lors de la détection d'intention: {e}")
            # En cas d'erreur, accepter la demande par défaut
            return True, "Détection d'intention non disponible"
    
    async def enrich_market_query(self, user_input: str) -> str:
        """
        Enrichit et clarifie le prompt utilisateur pour optimiser la recherche Tavily
        
        Args:
            user_input: Le prompt original de l'utilisateur
        
        Returns:
            str: Prompt enrichi et structuré
        """
        
        if not self.is_configured():
            return user_input
        
        try:
            enrichment_prompt = """Tu es un expert en formulation de requêtes d'analyse de marché.

Ton rôle : transformer un prompt utilisateur en une requête structurée et optimisée pour un moteur de recherche.

Instructions :
- Ajoute du contexte pertinent implicite
- Précise le périmètre géographique si non mentionné (France/Europe par défaut)
- Structure la requête avec des mots-clés pertinents
- Ajoute des aspects clés d'analyse (tendances, acteurs, données chiffrées)
- Reste concis (max 2-3 phrases)
- Utilise un langage adapté à la recherche web professionnelle

Réponds UNIQUEMENT par la requête enrichie, sans préambule ni explication."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": enrichment_prompt},
                    {"role": "user", "content": f"Prompt à enrichir : {user_input}"}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            enriched_query = response.choices[0].message.content.strip()
            print(f"📝 Prompt enrichi : {enriched_query}")
            return enriched_query
            
        except Exception as e:
            print(f"Erreur lors de l'enrichissement: {e}")
            return user_input
    
    async def _enrich_for_datasets(self, user_query: str) -> str:
        """
        Enrichit spécifiquement pour trouver des datasets pertinents
        Ajoute des termes techniques et statistiques précis
        """
        if not self.is_configured():
            return user_query
        
        try:
            prompt = f"""Transforme cette requête pour trouver des DATASETS spécifiques (CSV/Excel) sur le sujet.

Requête: "{user_query}"

Règles:
- Identifier les termes EXACTS pour des datasets (ex: "immatriculations véhicules électriques" plutôt que "marché automobile")
- Ajouter des qualificatifs statistiques: données, chiffres, statistiques, séries temporelles
- Inclure des termes techniques du domaine
- Préciser la zone géographique si pertinent (France, région, etc.)
- Répondre UNIQUEMENT par la requête (max 12 mots)

Exemples:
"marché véhicules électriques" → "immatriculations véhicules électriques hybrides rechargeables France statistiques ventes"
"opportunités IA" → "intelligence artificielle investissements déploiement France données chiffres marché"
"immobilier Paris" → "prix immobilier transactions logements Paris Ile-de-France données notaires"

Requête pour datasets:"""
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un expert en recherche de données statistiques."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=80
            )
            
            enriched = response.choices[0].message.content.strip()
            return enriched if enriched else user_query
            
        except Exception as e:
            print(f"⚠️ Erreur enrichissement datasets: {e}")
            return user_query
    
    async def format_tavily_response(self, tavily_results: List, user_query: str) -> str:
        """
        Reformule les résultats Tavily en français structuré et professionnel
        
        Args:
            tavily_results: Liste des résultats de recherche Tavily
            user_query: La requête originale de l'utilisateur
        
        Returns:
            str: Analyse formatée en français
        """
        
        if not self.is_configured():
            return self._generate_mock_response(user_query)
        
        try:
            # Extraire le contenu des résultats Tavily (ce sont des objets SearchResult)
            context = "\n\n".join([
                f"Source {i+1}: {result.title}\n{result.snippet}"
                for i, result in enumerate(tavily_results[:5])
            ])
            
            formatting_prompt = """Tu es un analyste de marché professionnel. 

Ton rôle : synthétiser des informations brutes de recherche web en une analyse de marché structurée, claire et professionnelle en français.

Instructions :
- Utilise un français impeccable et professionnel
- Structure l'analyse avec des sections claires (tendances, acteurs, opportunités, etc.)
- Utilise des puces pour les listes
- Mets en gras (**texte**) les points importants
- Cite les chiffres et données factuelles quand disponibles
- Reste objectif et factuel
- Longueur : 300-500 mots

Format souhaité :
**Analyse de marché : [Sujet]**

**Vue d'ensemble**
[Contexte général]

**Tendances principales**
• Point 1
• Point 2

**Acteurs clés**
[Description]

**Opportunités**
• Opportunité 1

**Recommandations**
[Synthèse]"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": formatting_prompt},
                    {"role": "user", "content": f"Requête utilisateur : {user_query}\n\nInformations collectées :\n{context}\n\nRédige l'analyse de marché."}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            formatted_response = response.choices[0].message.content.strip()
            return formatted_response
            
        except Exception as e:
            print(f"Erreur lors du formatage: {e}")
            return self._generate_mock_response(user_query)
    async def analyze_user_input(self, user_input: str) -> str:
        """
        Analyse l'entrée utilisateur avec détection d'intention et enrichissement
        
        Flux :
        1. Détecte si c'est une demande d'analyse de marché
        2. Si non : refuse et demande de reformuler
        3. Si oui : enrichit le prompt, appelle Tavily, reformule la réponse
        
        Args:
            user_input: La requête de l'utilisateur depuis la ChatBox
        
        Returns:
            str: Réponse générée (analyse ou message d'erreur)
        """
        
        print(f"🔍 Analyse de la requête : {user_input}")
        
        # Étape 1 : Détection d'intention
        is_market_analysis, explanation = await self.detect_market_analysis_intent(user_input)
        
        if not is_market_analysis:
            print(f"❌ Intention non valide : {explanation}")
            return {"response": f"""**Demande non compatible avec l'analyse de marché**

Votre demande ne semble pas correspondre à une analyse de marché.

**Raison** : {explanation}

**Pour obtenir une analyse de marché, veuillez reformuler votre demande en précisant :**
• Le secteur ou l'industrie à analyser
• Le type d'information recherché (tendances, concurrence, opportunités)
• Le périmètre géographique si pertinent

**Exemples de requêtes valides :**
• "Analyse du marché des véhicules électriques en Europe"
• "Tendances du e-commerce en France"
• "Opportunités dans le secteur de l'intelligence artificielle"
• "Analyse de la concurrence dans le marché du luxe"

N'hésitez pas à reformuler votre demande ! 🔍""", "sources": [], "datasets": []}
        
        print(f"✅ Intention valide : {explanation}")
        
        # Étape 2 : Enrichissement du prompt
        enriched_query = await self.enrich_market_query(user_input)
        
        # Étape 3 : Recherche Tavily pour le contexte textuel uniquement
        if self.tavily_service and self.tavily_service.is_configured():
            print(f"🌐 Recherche Tavily avec : {enriched_query}")
            try:
                # Recherche générale pour le contexte
                tavily_general_results = await self.tavily_service.search(
                    query=enriched_query,
                    mode="general",
                    max_results=5
                )
                
                # Gérer les erreurs potentielles
                if isinstance(tavily_general_results, Exception):
                    print(f"⚠️ Erreur recherche générale: {tavily_general_results}")
                    tavily_general_results = []
                
                print(f"📊 Tavily général: {len(tavily_general_results)} résultats")
                
                # Si aucun résultat, utiliser le LLM direct
                if not tavily_general_results or len(tavily_general_results) == 0:
                    print("⚠️ Aucun résultat Tavily - Basculement vers LLM direct")
                    response = await self._direct_llm_response(user_input)
                    return {"response": response, "sources": []}
                
                # Étape 4 : Reformulation de la réponse Tavily
                formatted_response = await self.format_tavily_response(tavily_general_results, user_input)
                
                # Préparer les sources pour le frontend
                sources_data = [{
                    "title": result.title,
                    "url": result.url
                } for result in tavily_general_results]
                
                # Retourner avec sources uniquement (pas de datasets pour l'instant)
                return {
                    "response": formatted_response,
                    "sources": sources_data
                }
                
            except Exception as e:
                print(f"⚠️ Erreur Tavily : {e}")
                # Fallback : réponse directe du LLM sans Tavily
                response = await self._direct_llm_response(user_input)
                return {"response": response, "sources": []}
        else:
            print("⚠️ Tavily non configuré - Réponse LLM directe")
            # Fallback : réponse directe du LLM sans Tavily
            response = await self._direct_llm_response(user_input)
            return {"response": response, "sources": []}
    
    def _is_dataset_url(self, url: str) -> bool:
        """Vérifie si une URL pointe vers un dataset"""
        url_lower = url.lower()
        return any(url_lower.endswith(ext) for ext in ['.csv', '.xlsx', '.xls'])
    
    def _detect_file_type(self, url: str) -> str:
        """Détecte le type de fichier depuis l'URL"""
        url_lower = url.lower()
        if url_lower.endswith('.csv'):
            return 'csv'
        elif url_lower.endswith(('.xlsx', '.xls')):
            return 'excel'
        return 'unknown'
    
    async def _validate_datasets_relevance(self, datasets: List[Dict], user_query: str) -> List[Dict]:
        """
        Valide la pertinence des datasets trouvés par rapport à la requête utilisateur
        
        Args:
            datasets: Liste des datasets trouvés avec title et url
            user_query: La requête originale de l'utilisateur
        
        Returns:
            Liste filtrée des datasets pertinents uniquement
        """
        
        if not self.is_configured():
            # En mode non configuré, retourner tous les datasets
            return datasets
        
        try:
            # Préparer la liste des datasets pour le LLM
            datasets_info = "\n".join([
                f"{i+1}. Titre: {ds['title']}\n   URL: {ds['url']}"
                for i, ds in enumerate(datasets)
            ])
            
            validation_prompt = f"""Tu es un expert en évaluation de pertinence de données pour l'analyse de marché.

Requête utilisateur: "{user_query}"

Datasets trouvés:
{datasets_info}

Ton rôle: Évaluer si chaque dataset est DIRECTEMENT PERTINENT pour répondre à la requête.

Critères de pertinence STRICTS:
- Le dataset doit traiter SPÉCIFIQUEMENT du sujet demandé (pas seulement un sujet connexe)
- Vérifier la zone géographique: un dataset régional (ex: Guadeloupe) n'est PAS pertinent pour une analyse France entière
- Vérifier la granularité: "transport en général" n'est PAS pertinent pour "véhicules électriques"
- Le titre/colonnes doivent clairement indiquer des données sur le sujet exact

REJETER si:
- Le dataset est trop générique (ex: "transport" pour "véhicules électriques")
- La zone géographique ne correspond pas (région vs national)
- Le sujet est connexe mais pas le même (ex: "automobiles en général" vs "véhicules électriques")

ACCEPTER seulement si:
- Le sujet exact est traité (pas juste le domaine général)
- La zone géographique correspond
- Les données sont exploitables et spécifiques

Réponds UNIQUEMENT par un JSON avec ce format exact:
{{
  "relevant_indices": [1, 3],  // Indices des datasets pertinents (commence à 1)
  "explanation": "Dataset X: score 8/10 car [raison précise]. Dataset Y: score 3/10 car [raison du rejet]."
}}

Ne réponds QUE par le JSON, rien d'autre."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": validation_prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            relevant_indices = result.get("relevant_indices", [])
            explanation = result.get("explanation", "")
            
            print(f"🔍 Validation LLM: {explanation}")
            
            # Filtrer les datasets selon les indices pertinents (convertir de 1-indexed à 0-indexed)
            relevant_datasets = [datasets[i-1] for i in relevant_indices if 0 < i <= len(datasets)]
            
            return relevant_datasets
            
        except Exception as e:
            print(f"⚠️ Erreur validation pertinence: {e}")
            # En cas d'erreur, retourner tous les datasets pour ne pas bloquer
            return datasets
    
    async def _direct_llm_response(self, user_input: str) -> str:
        """
        Génère une réponse directe du LLM sans recherche Tavily (fallback)
        """
        
        if not self.is_configured():
            return self._generate_mock_response(user_input)
        
        try:
            system_prompt = """Tu es un outil d'analyse de marché expert. 
Tu aides les utilisateurs à analyser les marchés, les tendances, les concurrents et les opportunités d'affaires.
Réponds de manière structurée, professionnelle et actionnable en français.
Utilise des puces, du gras (**texte**) et structure ton analyse clairement."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erreur lors de l'appel à OpenAI: {e}")
            return self._generate_mock_response(user_input)
    
    async def validate_dataset_content(self, dataset_keywords: str, user_query: str) -> bool:
        """
        Valide la pertinence d'un dataset en analysant ses colonnes et contenu
        
        Args:
            dataset_keywords: String contenant colonnes et premières valeurs du dataset
            user_query: Requête utilisateur originale
        
        Returns:
            True si le dataset est pertinent, False sinon
        """
        if not self.is_configured() or not dataset_keywords:
            return True  # Fallback: accepter si pas de LLM
        
        try:
            prompt = f"""Analyse si ce dataset est pertinent pour la requête utilisateur.

Requête: "{user_query}"

Contenu du dataset:
{dataset_keywords}

Le dataset est-il DIRECTEMENT pertinent pour répondre à la requête ?

Critères STRICTS:
- Les colonnes doivent traiter du sujet exact (pas juste un domaine connexe)
- Rejeter si trop générique (ex: "transport" vs "véhicules électriques")
- Rejeter si zone géographique incorrecte (ex: Guadeloupe vs France)

Réponds UNIQUEMENT par "OUI" ou "NON" (un seul mot)."""

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un expert en évaluation de pertinence de données."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            answer = response.choices[0].message.content.strip().upper()
            is_relevant = "OUI" in answer
            
            print(f"  🔍 Validation contenu: {'✅ Pertinent' if is_relevant else '❌ Non pertinent'}")
            return is_relevant
            
        except Exception as e:
            print(f"⚠️ Erreur validation contenu: {e}")
            return True  # En cas d'erreur, accepter pour ne pas bloquer
    
    def _generate_mock_response(self, user_input: str) -> str:
        """Génère une réponse mock pour les tests"""
        return f"""**Analyse de marché pour: {user_input}**

Voici une analyse préliminaire basée sur votre demande:

**Tendances actuelles:**
- Le marché montre des signes de croissance continue
- L'innovation technologique reste un facteur clé
- Les consommateurs privilégient la durabilité

**Recommandations:**
- Surveiller les évolutions réglementaires
- Investir dans les technologies émergentes
- Développer une stratégie de différenciation

*Note: Cette analyse est générée en mode simulation. Configurez une clé API OpenAI pour obtenir des analyses plus détaillées.*"""
    
    async def generate_analysis(
        self,
        query: str,
        web_context: str = "",
        sources: List = None
    ) -> Dict:
        
        """
        Génère une analyse de marché complète
        
        Args:
            query: La requête utilisateur
            web_context: Contexte des recherches web
            sources: Liste des sources utilisées
        
        Returns:
            Dict contenant qualitative et quantitative
        """
        
        # Si pas configuré, utiliser des données mock
        if not self.is_configured():
            return self._generate_mock_analysis(query, sources)
        
        # TODO: Implémenter l'appel réel au LLM avec LangChain
        # Pour l'instant, retourner des données mock
        return self._generate_mock_analysis(query, sources)
    
    def _generate_mock_analysis(self, query: str, sources: List = None) -> Dict:
        """Génère une analyse mock basée sur la requête"""
        
        # Extraire le sujet principal
        subject = query.lower()
        
        # Créer des sources URLs si disponibles
        source_urls = []
        if sources:
            source_urls = [s.url for s in sources[:5]]
        
        # Générer l'analyse qualitative
        qualitative = {
            "title": f"Analyse Qualitative - {query.title()}",
            "sections": [
                {
                    "subtitle": "Vue d'ensemble du marché",
                    "content": f"Le marché {subject} connaît une croissance dynamique portée par l'innovation technologique et l'évolution des comportements des consommateurs. Les données récentes montrent une transformation structurelle du secteur avec l'émergence de nouveaux acteurs et modèles économiques."
                },
                {
                    "subtitle": "Tendances principales",
                    "content": f"• Digitalisation accélérée des processus et services\n• Croissance de la demande pour des solutions durables\n• Consolidation du marché avec des fusions-acquisitions\n• Innovation continue dans les technologies de pointe\n• Expansion internationale des principaux acteurs"
                },
                {
                    "subtitle": "Acteurs principaux",
                    "content": f"Le marché {subject} est dominé par plusieurs acteurs majeurs qui investissent massivement dans l'innovation et l'expansion. Les leaders du marché bénéficient d'économies d'échelle importantes tandis que de nouveaux entrants apportent disruption et innovation."
                },
                {
                    "subtitle": "Opportunités",
                    "content": f"• Forte demande dans les segments premium\n• Marchés émergents en pleine croissance\n• Technologies disruptives créant de nouvelles niches\n• Partenariats stratégiques et écosystèmes\n• Services à valeur ajoutée et personnalisation"
                },
                {
                    "subtitle": "Défis et risques",
                    "content": f"• Concurrence intense et guerre des prix\n• Réglementations de plus en plus strictes\n• Volatilité des coûts des matières premières\n• Cybersécurité et protection des données\n• Changements rapides des préférences consommateurs"
                }
            ],
            "recommendation": f"Le marché {subject} offre des opportunités stratégiques significatives. Nous recommandons une approche focalisée sur l'innovation, la différenciation et l'expansion géographique ciblée pour maximiser la croissance.",
            "sources": source_urls
        }
        
        # Générer les données quantitatives
        quantitative = {
            "marketSize": {
                "labels": ["2021", "2022", "2023", "2024", "2025 (proj.)"],
                "data": [100, 125, 156, 195, 244],
                "unit": "milliards €",
                "sources": source_urls[:2] if source_urls else []
            },
            "marketShare": {
                "labels": ["Leader A", "Leader B", "Leader C", "Leader D", "Autres"],
                "data": [25, 18, 15, 12, 30],
                "colors": ["#0055B8", "#00A9E0", "#7AC143", "#FDB913", "#95A5A6"],
                "sources": source_urls[2:4] if len(source_urls) > 2 else []
            },
            "regionalGrowth": {
                "labels": ["Europe", "Amérique du Nord", "Asie-Pacifique", "Amérique Latine", "MEA"],
                "data": [35, 28, 25, 8, 4],
                "growth": [12.5, 15.8, 22.3, 18.5, 14.2],
                "sources": source_urls[4:6] if len(source_urls) > 4 else []
            },
            "priceEvolution": {
                "labels": ["2020", "2021", "2022", "2023", "2024"],
                "avgPrice": [100, 105, 108, 110, 112],
                "marketValue": [85, 100, 125, 156, 195],
                "sources": source_urls[-2:] if len(source_urls) > 1 else []
            }
        }
        
        return {
            "qualitative": qualitative,
            "quantitative": quantitative
        }
