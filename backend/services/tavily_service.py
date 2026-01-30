"""
Service de recherche web avec Tavily
Gère les deux modes : general et data
"""

import httpx
from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    published_at: Optional[datetime] = None
    source_type: Literal["market_report", "news", "gov_data", "other"]
    reliability_score: int


class TavilyService:
    """Service pour effectuer des recherches via l'API Tavily"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com"
        
        # Domaines fiables par type
        self.trusted_domains = {
            "gov_data": [".gov", ".gouv", ".europa.eu", ".oecd.org"],
            "market_report": [
                "statista.com", "gartner.com", "forrester.com", 
                "mckinsey.com", "bcg.com", "kpmg.com", "deloitte.com",
                "pwc.com", "accenture.com"
            ],
            "news": [
                "lesechos.fr", "ft.com", "wsj.com", "bloomberg.com",
                "reuters.com", "economist.com", "challenges.fr"
            ]
        }
    
    def is_configured(self) -> bool:
        """Vérifie si le service est configuré avec une clé API"""
        return self.api_key is not None and self.api_key != "your_tavily_api_key_here"
    
    def _classify_source(self, url: str) -> tuple[str, int]:
        """
        Classifie la source et attribue un score de fiabilité
        Returns: (source_type, reliability_score)
        """
        url_lower = url.lower()
        
        # Vérifier les domaines gouvernementaux (score élevé)
        for domain in self.trusted_domains["gov_data"]:
            if domain in url_lower:
                return "gov_data", 95
        
        # Vérifier les rapports de cabinets d'analyse
        for domain in self.trusted_domains["market_report"]:
            if domain in url_lower:
                return "market_report", 90
        
        # Vérifier les médias économiques reconnus
        for domain in self.trusted_domains["news"]:
            if domain in url_lower:
                return "news", 85
        
        # Autres sources (score acceptable pour des analyses générales)
        return "other", 70
    
    def _filter_by_reliability(
        self, 
        results: List[SearchResult], 
        min_score: int = 70
    ) -> List[SearchResult]:
        """Filtre les résultats selon le score de fiabilité"""
        filtered = [r for r in results if r.reliability_score >= min_score]
        print(f"🔍 Filtrage : {len(results)} résultats -> {len(filtered)} résultats (seuil: {min_score})")
        
        # Si trop peu de résultats après filtrage, afficher les scores
        if len(filtered) < 3:
            print(f"⚠️ Scores des résultats: {[r.reliability_score for r in results]}")
        
        return filtered
    
    async def search(
        self,
        query: str,
        mode: Literal["general", "data"] = "general",
        max_results: int = 10
    ) -> List[SearchResult]:
        """
        Effectue une recherche via Tavily
        
        Args:
            query: Requête de recherche
            mode: "general" pour contexte général, "data" pour données quantitatives
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de SearchResult
        """
        
        # Si Tavily n'est pas configuré, lever une exception
        if not self.is_configured():
            raise Exception("Tavily n'est pas configuré. Veuillez ajouter une clé API valide.")
        
        try:
            # Mode général uniquement (data mode supprimé)
            search_query = query
            search_depth = "basic"
            
            # Appel à l'API Tavily
            tavily_params = {
                "api_key": self.api_key,
                "query": search_query,
                "max_results": max_results or 10,
                "search_depth": search_depth
            }
            
            print(f"🔍 Tavily params: query='{search_query}'")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json=tavily_params,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    print(f"❌ Tavily API error: {response.status_code}")
                    print(f"Response: {response.text}")
                    raise Exception(f"Tavily API error: {response.status_code}")
                
                data = response.json()
                print(f"🔍 Réponse Tavily brute: {data}")
                results = self._parse_tavily_response(data)
                
                # Filtrer par fiabilité
                results = self._filter_by_reliability(results, min_score=60)
                
                # Si aucun résultat après filtrage, garder tous les résultats
                if len(results) == 0:
                    print("⚠️ Aucun résultat après filtrage - Conservation de tous les résultats")
                    results = self._parse_tavily_response(data)
                
                return results[:max_results]
        
        except Exception as e:
            print(f"Erreur lors de la recherche Tavily: {e}")
            raise Exception(f"Échec de la recherche Tavily: {str(e)}")
    
    def _get_preferred_domains(self, mode: str) -> List[str]:
        """Retourne les domaines préférés selon le mode"""
        if mode == "data":
            # Pour le mode data, FORCER uniquement INSEE et portails français
            return [
                "insee.fr",
                "data.gouv.fr",
                "statistiques.developpement-durable.gouv.fr"
            ]
        return []
    
    def _boost_dataset_urls(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Booste le score de fiabilité des URLs qui semblent contenir des datasets
        Filtre aussi les URLs API non pertinentes
        """
        boosted_results = []
        for result in results:
            url_lower = result.url.lower()
            title_lower = result.title.lower()
            
            # FILTRAGE : Exclure complètement les URLs API
            if '/api/' in url_lower or url_lower.endswith('.xml'):
                print(f"  ❌ Exclusion URL API/XML: {result.url}")
                continue
            
            # Critères de boost
            boost = 0
            if '/statistiques/' in url_lower:
                boost += 20  # Boost fort pour pages statistiques
            if '/fichier/' in url_lower:
                boost += 15
            if 'insee.fr' in url_lower:
                boost += 10
            if any(keyword in title_lower for keyword in ['données', 'statistique', 'chiffres', 'tableau']):
                boost += 5
            
            # Appliquer le boost
            new_score = min(100, result.reliability_score + boost)
            
            if boost > 0:
                print(f"  📈 Boost +{boost} pour {result.url} (score: {result.reliability_score} → {new_score})")
            
            boosted_result = SearchResult(
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                source_type=result.source_type,
                reliability_score=new_score
            )
            boosted_results.append(boosted_result)
        
        # Trier par score après boost
        return sorted(boosted_results, key=lambda x: x.reliability_score, reverse=True)  # Pas de filtre strict en mode général
    
    def _parse_tavily_response(self, data: dict) -> List[SearchResult]:
        """Parse la réponse de l'API Tavily"""
        results = []
        
        # Vérifier différentes clés possibles dans la réponse
        results_data = data.get("results", data.get("data", data.get("items", [])))
        print(f"📋 Nombre de résultats bruts Tavily: {len(results_data)}")
        
        for item in results_data:
            source_type, reliability_score = self._classify_source(item.get("url", ""))
            
            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", "")[:300],
                published_at=self._parse_date(item.get("published_date")),
                source_type=source_type,
                reliability_score=reliability_score
            )
            results.append(result)
        
        return results
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse une date depuis une chaîne"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            return None
    
    def format_context_for_llm(self, results: List[SearchResult]) -> str:
        """Formate les résultats de recherche pour le contexte du LLM"""
        context = "Contexte basé sur les recherches web:\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"{i}. {result.title}\n"
            context += f"   Source: {result.url} (Fiabilité: {result.reliability_score}/100)\n"
            context += f"   {result.snippet}\n\n"
        
        return context
