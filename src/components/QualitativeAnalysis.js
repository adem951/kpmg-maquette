import React from 'react';
import './QualitativeAnalysis.css';

const QualitativeAnalysis = ({ data }) => {
  if (!data) return null;

  const { title, sections, recommendation, sources } = data;

  return (
    <div className="qualitative-analysis">
      <h2>📝 {title}</h2>
      
      {sources && sources.length > 0 && (
        <div className="sources-banner">
          <span className="sources-icon">🔗</span>
          <span>{sources.length} sources fiables consultées</span>
        </div>
      )}
      
      <div className="analysis-sections">
        {sections.map((section, index) => (
          <div key={index} className="analysis-section">
            <h3>{section.subtitle}</h3>
            <div className="section-content">
              {section.content.split('\n').map((paragraph, pIndex) => (
                <p key={pIndex}>{paragraph}</p>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="recommendation-box">
        <div className="recommendation-header">
          <span className="recommendation-icon">💡</span>
          <h3>Recommandations Stratégiques</h3>
        </div>
        <p>{recommendation}</p>
      </div>

      {sources && sources.length > 0 && (
        <div className="sources-list">
          <h3>📚 Sources consultées</h3>
          <ul>
            {sources.slice(0, 5).map((source, index) => (
              <li key={index}>
                <a href={source} target="_blank" rel="noopener noreferrer">
                  {source}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="analysis-footer">
        <div className="footer-info">
          <span className="info-item">
            <strong>🕒 Date d'analyse:</strong> {new Date().toLocaleDateString('fr-FR', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </span>
          <span className="info-item">
            <strong>🤖 Généré par:</strong> IA KPMG Market Analysis
          </span>
          <span className="info-item">
            <strong>📊 Type:</strong> Analyse Qualitative Approfondie
          </span>
        </div>
        <button className="export-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M7 10L12 15L17 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M12 15V3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Exporter le rapport (PDF)
        </button>
      </div>
    </div>
  );
};

export default QualitativeAnalysis;
