import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import QualitativeAnalysis from './components/QualitativeAnalysis';
import QuantitativeAnalysis from './components/QuantitativeAnalysis';
import { getAnalysis } from './mockData';
import './App.css';

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleAnalysisRequest = (query) => {
    // Simuler le chargement
    setShowResults(false);
    
    setTimeout(() => {
      const analysis = getAnalysis(query);
      setCurrentAnalysis(analysis);
      setShowResults(true);
    }, 1000);
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
            <ChatBox onSendMessage={handleAnalysisRequest} />
          </div>

          <div className="right-panel">
            {!showResults ? (
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
                    <QualitativeAnalysis data={currentAnalysis.qualitative} />
                    <QuantitativeAnalysis data={currentAnalysis.quantitative} />
                  </>
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
