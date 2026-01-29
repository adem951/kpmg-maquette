import React from 'react';
import './QuantitativeAnalysis.css';

const QuantitativeAnalysis = ({ sources = [], datasets = [] }) => {
  console.log('📊 QuantitativeAnalysis - Sources:', sources);
  console.log('📊 QuantitativeAnalysis - Datasets:', datasets);
  
  return (
    <div className="quantitative-analysis">
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

      {datasets && datasets.length > 0 && (
        <div className="datasets-section">
          <h3>📊 Datasets trouvés</h3>
          {datasets.map((dataset, index) => (
            <div key={index} className="dataset-card">
              <div className="dataset-header">
                <h4>{dataset.title}</h4>
                <span className="dataset-badge">{dataset.format.toUpperCase()}</span>
              </div>
              
              <div className="dataset-info">
                <p><strong>Total de lignes:</strong> {dataset.total_rows}</p>
                <p><strong>Colonnes:</strong> {dataset.columns.join(', ')}</p>
                <a 
                  href={dataset.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="dataset-link"
                >
                  Télécharger le dataset →
                </a>
              </div>
              
              <div className="dataset-preview">
                <h5>Aperçu (5 premières lignes)</h5>
                <div className="table-wrapper">
                  <table className="preview-table">
                    <thead>
                      <tr>
                        {dataset.columns.map((col, colIndex) => (
                          <th key={colIndex}>{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {dataset.preview.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                          {dataset.columns.map((col, colIndex) => (
                            <td key={colIndex}>{row[col] !== null && row[col] !== undefined ? String(row[col]) : '-'}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QuantitativeAnalysis;
