"""
Service de gestion des données
Abstraction pour faciliter l'ajout futur d'une BDD
"""

from typing import Dict, List, Optional
from datetime import datetime


class DataService:
    """
    Service d'abstraction pour la gestion des données
    Prêt pour l'intégration future d'une BDD (PostgreSQL ou MongoDB)
    """
    
    def __init__(self):
        # Pour l'instant, stockage en mémoire
        # À remplacer par une vraie connexion BDD
        self.db_type = None  # 'postgresql' ou 'mongodb'
        self.connection = None
    
    # --- Méthodes pour la BDD future ---
    
    def connect_database(self, db_type: str, connection_string: str):
        """
        Connecte à une base de données
        À implémenter plus tard selon le type de BDD choisi
        """
        self.db_type = db_type
        # TODO: Implémenter la connexion réelle
        pass
    
    async def get_market_data(self) -> List[Dict]:
        """
        Récupère les données de marché depuis la BDD
        Pour l'instant, retourne des données mock
        """
        # TODO: Remplacer par une vraie requête BDD
        return [
            {
                "id": 1,
                "année": 2023,
                "tailleMarché": 150,
                "pays": "FR",
                "secteur": "Technologie",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 2,
                "année": 2024,
                "tailleMarché": 175,
                "pays": "FR",
                "secteur": "Technologie",
                "created_at": datetime.now().isoformat()
            }
        ]
    
    async def save_market_data(self, data: Dict) -> str:
        """
        Sauvegarde les données de marché dans la BDD
        Pour l'instant, simule uniquement la sauvegarde
        """
        # TODO: Implémenter la sauvegarde réelle en BDD
        print(f"[DATA SERVICE] Données à sauvegarder: {data}")
        return "mock_id_123"
    
    async def query_market_data(
        self,
        filters: Dict,
        limit: int = 100
    ) -> List[Dict]:
        """
        Requête personnalisée sur les données de marché
        """
        # TODO: Implémenter les requêtes avec filtres
        return await self.get_market_data()
    
    # --- Méthodes de formatage ---
    
    def format_quantitative_data(
        self,
        analysis_data: Dict,
        sources: List
    ) -> Dict:
        """
        Formate les données quantitatives pour les graphiques
        Ajoute les sources et s'assure du bon format
        """
        
        # Extraire les URLs des sources
        source_urls = [s.url for s in sources] if sources else []
        
        # S'assurer que chaque dataset a des sources
        if "marketSize" in analysis_data:
            if "sources" not in analysis_data["marketSize"]:
                analysis_data["marketSize"]["sources"] = source_urls[:2]
        
        if "marketShare" in analysis_data:
            if "sources" not in analysis_data["marketShare"]:
                analysis_data["marketShare"]["sources"] = source_urls[2:4]
        
        if "regionalGrowth" in analysis_data:
            if "sources" not in analysis_data["regionalGrowth"]:
                analysis_data["regionalGrowth"]["sources"] = source_urls[4:6]
        
        if "priceEvolution" in analysis_data:
            if "sources" not in analysis_data["priceEvolution"]:
                analysis_data["priceEvolution"]["sources"] = source_urls[-2:]
        
        return analysis_data
    
    def validate_data_format(self, data: Dict) -> bool:
        """
        Valide que les données sont au bon format pour le frontend
        """
        required_fields = ["labels", "data"]
        
        if not all(field in data for field in required_fields):
            return False
        
        if len(data["labels"]) != len(data["data"]):
            return False
        
        return True
    
    # --- Méthodes pour la connexion BDD future ---
    
    def _get_postgresql_connection(self, connection_string: str):
        """Crée une connexion PostgreSQL (à implémenter)"""
        # from sqlalchemy import create_engine
        # engine = create_engine(connection_string)
        # return engine
        pass
    
    def _get_mongodb_connection(self, connection_string: str):
        """Crée une connexion MongoDB (à implémenter)"""
        # from pymongo import MongoClient
        # client = MongoClient(connection_string)
        # return client
        pass
    
    def _execute_sql_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute une requête SQL (à implémenter)"""
        # if self.db_type != 'postgresql':
        #     raise ValueError("Not a SQL database")
        # 
        # with self.connection.connect() as conn:
        #     result = conn.execute(query, params or {})
        #     return [dict(row) for row in result]
        pass
    
    def _execute_mongodb_query(self, collection: str, filter: Dict) -> List[Dict]:
        """Execute une requête MongoDB (à implémenter)"""
        # if self.db_type != 'mongodb':
        #     raise ValueError("Not a MongoDB database")
        # 
        # db = self.connection['market_analysis']
        # collection = db[collection]
        # return list(collection.find(filter))
        pass
