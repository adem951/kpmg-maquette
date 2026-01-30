import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import QualitativeAnalysis from './components/QualitativeAnalysis';
import QuantitativeAnalysis from './components/QuantitativeAnalysis';
import './App.css';

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchedDatasets, setSearchedDatasets] = useState([]);
  const [activeTab, setActiveTab] = useState('qualitative'); // 'qualitative' ou 'quantitative'

  const handleAnalysisRequest = (query, response) => {
    setIsLoading(true);
    setError(null);
    setShowResults(false);
    setActiveTab('qualitative'); // Par défaut, afficher l'analyse qualitative
    
    // Si la réponse est fournie directement (depuis l'API LLM)
    if (response) {
      // Gérer le nouveau format avec sources et datasets
      const analysisData = {
        llmResponse: typeof response === 'object' && response.response ? response.response : response,
        sources: typeof response === 'object' && response.sources ? response.sources : [],
        datasets: typeof response === 'object' && response.datasets ? response.datasets : [],
        query: query
      };
      
      console.log('📊 App.js - Données d\'analyse:', analysisData);
      console.log('📊 App.js - Datasets:', analysisData.datasets);
      
      setCurrentAnalysis(analysisData);
      setShowResults(true);
      setIsLoading(false);
    } else {
      // Fallback vers les données mock si l'API échoue
      setTimeout(() => {
        setCurrentAnalysis(null);
        setShowResults(false);
        setIsLoading(false);
        setError("Impossible de récupérer l'analyse. Veuillez réessayer.");
      }, 1000);
    }
  };

  const handleDatasetsFound = (datasets) => {
    console.log('📊 App.js - Datasets trouvés via API:', datasets);
    setSearchedDatasets(datasets);
    setShowResults(true);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">📊</div>
            <div className="logo-text">
              <h1>KPMG</h1>
              <span>Market Analysis Platform</span>
            </div>
          </div>
          <nav className="nav-menu">
            <button className="nav-item active">Dashboard</button>
            <button className="nav-item">Mes Analyses</button>
            <button className="nav-item">Rapports</button>
          </nav>
        </div>
      </header>

      <main className="app-main">
        <div className="main-container">
          <div className="left-panel">
            <div className="welcome-section">
              <h2>Bienvenue sur votre plateforme d'analyse de marché</h2>
              <p>Utilisez l'assistant IA pour obtenir des analyses détaillées en quelques secondes</p>
            </div>
            <ChatBox 
              onSendMessage={handleAnalysisRequest} 
              onDatasetsFound={handleDatasetsFound}
            />
          </div>

          <div className="right-panel">
            {isLoading ? (
              <div className="loading-content">
                <div className="loader"></div>
                <h3>Analyse en cours...</h3>
                <p>Recherche d'informations et génération de l'analyse de marché</p>
              </div>
            ) : error ? (
              <div className="error-content">
                <div className="error-icon">⚠️</div>
                <h3>Erreur</h3>
                <p>{error}</p>
                <button onClick={() => setError(null)}>Réessayer</button>
              </div>
            ) : !showResults ? (
              <div className="placeholder-content">
                <div className="placeholder-icon">🔍</div>
                <h3>Aucune analyse en cours</h3>
                <p>Posez une question à l'assistant IA pour démarrer une analyse de marché</p>
                <div className="example-queries">
                  <h4>Exemples de requêtes :</h4>
                  <ul>
                    <li>Analyse du marché des véhicules électriques</li>
                    <li>Marché du e-commerce en France</li>
                    <li>Tendances du secteur de la santé digitale</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="results-container">
                {currentAnalysis && (
                  <>
                    {/* Onglets de navigation */}
                    <div className="analysis-tabs">
                      <button 
                        className={`tab-btn ${activeTab === 'qualitative' ? 'active' : ''}`}
                        onClick={() => setActiveTab('qualitative')}
                      >
                        📝 Analyse Qualitative
                      </button>
                      <button 
                        className={`tab-btn ${activeTab === 'quantitative' ? 'active' : ''}`}
                        onClick={() => setActiveTab('quantitative')}
                      >
                        📊 Analyse Quantitative ({currentAnalysis.datasets?.length || 0})
                      </button>
                    </div>

                    {/* Contenu des onglets */}
                    <div className="tab-content">
                      {activeTab === 'qualitative' && (
                        <QualitativeAnalysis 
                          analysisData={currentAnalysis.llmResponse}
                          sources={currentAnalysis.sources || []}
                        />
                      )}
                      
                      {activeTab === 'quantitative' && (
                        <QuantitativeAnalysis 
                          datasets={currentAnalysis.datasets || []}
                        />
                      )}
                    </div>
                  </>
                )}
                {searchedDatasets.length > 0 && !currentAnalysis && (
                  <QuantitativeAnalysis 
                    datasets={searchedDatasets}
                  />
                )}
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <p>&copy; 2025 KPMG - Tous droits réservés</p>
          <div className="footer-links">
            <a href="#confidentialite">Confidentialité</a>
            <a href="#conditions">Conditions d'utilisation</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
