"""
Backend FastAPI pour l'analyse de marché KPMG
Gère les recherches Tavily, l'orchestration LLM et la préparation des données
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Optional, List
from datetime import datetime
import os

# Les variables d'environnement sont lues directement depuis le système
# Pas besoin de fichier .env
# Configurer les variables sous Windows PowerShell:
# $env:TAVILY_API_KEY="votre_clé_tavily"
# $env:OPENAI_API_KEY="votre_clé_openai"

# Import des services
from services.tavily_service import TavilyService
from services.llm_service import LLMService

# Initialisation de l'application
app = FastAPI(
    title="KPMG Market Analysis API",
    description="API pour l'analyse de marché avec recherche web et génération IA",
    version="1.0.0"
)

# Configuration CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des services avec variables d'environnement système
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Avertissement si les clés ne sont pas définies
if not tavily_api_key:
    print("⚠️ TAVILY_API_KEY non définie - Mode mock activé")
if not openai_api_key:
    print("⚠️ OPENAI_API_KEY non définie - Mode mock activé")

tavily_service = TavilyService(api_key=tavily_api_key)
llm_service = LLMService(api_key=openai_api_key)

# Modèles Pydantic
class SearchRequest(BaseModel):
    query: str
    mode: Literal["general", "data"] = "general"
    max_results: int = 10

class AnalysisRequest(BaseModel):
    query: str
    include_web_search: bool = True

class ChatRequest(BaseModel):
    message: str

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    published_at: Optional[datetime] = None
    source_type: Literal["market_report", "news", "gov_data", "other"]
    reliability_score: int

class MarketData(BaseModel):
    labels: List[str]
    data: List[float]
    unit: str
    sources: List[str]

class AnalysisResponse(BaseModel):
    qualitative: dict
    quantitative: dict
    sources: List[SearchResult]
    generated_at: datetime


# Routes de l'API
@app.get("/")
async def root():
    """Route racine pour vérifier l'état de l'API"""
    return {
        "status": "online",
        "service": "KPMG Market Analysis API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "tavily": tavily_service.is_configured(),
            "llm": llm_service.is_configured(),
        }
    }

@app.post("/api/search/general")
async def search_general(request: SearchRequest):
    """
    Recherche web en mode général (contexte, tendances, acteurs)
    """
    try:
        results = await tavily_service.search(
            query=request.query,
            mode="general",
            max_results=request.max_results
        )
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/data")
async def search_data(request: SearchRequest):
    """
    Recherche web en mode data (chiffres, statistiques, données quantitatives)
    """
    try:
        results = await tavily_service.search(
            query=request.query,
            mode="data",
            max_results=request.max_results
        )
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def analyze_chat_input(request: ChatRequest):
    """
    Analyse l'entrée utilisateur depuis la ChatBox avec le LLM
    """
    try:
        response = await llm_service.analyze_user_input(request.message)
        
        return {
            "success": True,
            "response": response,
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analysis")
async def generate_analysis(request: AnalysisRequest):
    """
    Génère une analyse de marché complète avec recherche web et LLM
    """
    try:
        # Étape 1: Recherche web si demandée
        sources = []
        web_context = ""
        
        if request.include_web_search:
            # Recherche générale pour le contexte
            general_results = await tavily_service.search(
                query=request.query,
                mode="general",
                max_results=5
            )
            
            
            
            sources = general_results
            web_context = tavily_service.format_context_for_llm(sources)
        
        # Étape 2: Génération de l'analyse par le LLM
        analysis = await llm_service.generate_analysis(
            query=request.query,
            web_context=web_context,
            sources=sources
        )
        
        
        return {
            "success": True,
            "analysis": {
                "qualitative": analysis.get("qualitative", {}),
                "sources": sources,
                "generated_at": datetime.now().isoformat()
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
