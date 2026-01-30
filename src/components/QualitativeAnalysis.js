import React from 'react';
import './QualitativeAnalysis.css';

const QualitativeAnalysis = ({ analysisData = null, sources = [] }) => {
  const formatAnalysisContent = (content) => {
    if (!content) return '';
    
    // Convertir le markdown simple en HTML
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Gras
      .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italique
      .replace(/^- (.*$)/gim, '• $1') // Puces
      .split('\n')
      .map(line => line.trim())
      .filter(line => line !== '')
      .join('\n');
  };

  if (!analysisData) {
    return (
      <div className="qualitative-analysis">
        <div className="empty-state">
          <h2>📊 Données Qualitatives</h2>
          <p>Utilisez la chatbox pour obtenir une analyse de marché personnalisée.</p>
          <div className="suggestions">
            <p><strong>Exemples de requêtes :</strong></p>
            <ul>
              <li>• Analyse du marché des véhicules électriques en Europe</li>
              <li>• Tendances du e-commerce en France</li>
              <li>• Opportunités dans le secteur de l'IA</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="qualitative-analysis">
      <div className="analysis-header">
        <h2>📊 Analyse Qualitative</h2>
        <div className="timestamp">
          Générée le {new Date().toLocaleDateString('fr-FR')} à {new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
      
      <div className="analysis-content">
        <div className="content-body">
          {formatAnalysisContent(analysisData).split('\n').map((line, index) => (
            <p key={index} dangerouslySetInnerHTML={{ __html: line }} />
          ))}
        </div>
      </div>

      {/* Sources utilisées */}
      {sources && sources.length > 0 && (
        <div className="sources-section">
          <h3>📚 Sources utilisées</h3>
          <ul className="sources-list">
            {sources.map((source, index) => (
              <li key={index}>
                <a 
                  href={source.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="source-link"
                >
                  {source.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default QualitativeAnalysis;
