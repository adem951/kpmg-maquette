"""
Service LLM pour générer les analyses de marché
Utilise OpenAI GPT pour orchestrer l'analyse
"""

from typing import List, Dict, Optional
import json
import openai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class LLMService:
    """Service pour générer des analyses avec un LLM"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Modèle plus récent et économique
        
        # Configurer OpenAI
        if self.api_key:
            openai.api_key = self.api_key
    
    def is_configured(self) -> bool:
        """Vérifie si le service est configuré"""
        return self.api_key is not None and self.api_key != "your_openai_api_key_here"
    
    async def analyze_user_input(self, user_input: str) -> str:
        """
        Analyse l'entrée utilisateur avec un prompt système simple
        
        Args:
            user_input: La requête de l'utilisateur depuis la ChatBox
        
        Returns:
            str: Réponse générée par le LLM
        """
        
        if not self.is_configured():
            return self._generate_mock_response(user_input)
        
        try:
            # Prompt système pour l'outil d'analyse de marché
            system_prompt = """Tu es un outil d'analyse de marché expert. 
            Tu aides les utilisateurs à analyser les marchés, les tendances, les concurrents et les opportunités d'affaires.
            Réponds de manière structurée, professionnelle et actionnable.
            Utilise des informations factuelles quand possible et indique clairement quand tu fais des estimations ou des hypothèses."""
            
            response = openai.ChatCompletion.create(
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
