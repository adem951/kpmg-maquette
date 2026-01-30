import React, { useState } from 'react';
import { downloadDataset } from '../services/datasetService';
import './QuantitativeAnalysis.css';

const QuantitativeAnalysis = ({ datasets = [] }) => {
  const [downloadedDatasets, setDownloadedDatasets] = useState({});
  const [loadingDatasets, setLoadingDatasets] = useState({});
  
  console.log('📊 QuantitativeAnalysis - Datasets:', datasets);
  
  const handleDownload = async (dataset) => {
    setLoadingDatasets(prev => ({ ...prev, [dataset.url]: true }));
    
    try {
      const parsedData = await downloadDataset(dataset.url);
      setDownloadedDatasets(prev => ({
        ...prev,
        [dataset.url]: parsedData
      }));
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
      alert('Erreur lors du téléchargement du dataset');
    } finally {
      setLoadingDatasets(prev => ({ ...prev, [dataset.url]: false }));
    }
  };
  
  return (
    <div className="quantitative-analysis">
      {datasets && datasets.length > 0 && (
        <div className="datasets-section">
          <h3>📊 Datasets disponibles</h3>
          {datasets.map((dataset, index) => {
            const downloaded = downloadedDatasets[dataset.url];
            const isLoading = loadingDatasets[dataset.url];
            
            return (
              <div key={index} className="dataset-card">
                <div className="dataset-header">
                  <h4>{dataset.title}</h4>
                  {dataset.source && (
                    <span className="dataset-source-badge">{dataset.source}</span>
                  )}
                </div>
                
                <div className="dataset-info">
                  {dataset.description && (
                    <p className="dataset-description">{dataset.description}</p>
                  )}
                  {dataset.organization && (
                    <p><strong>Organisation:</strong> {dataset.organization}</p>
                  )}
                  {dataset.total_rows !== undefined && dataset.total_rows > 0 && (
                    <p><strong>Nombre de lignes:</strong> {dataset.total_rows.toLocaleString()}</p>
                  )}
                  
                  {/* Aperçu automatique si disponible */}
                  {dataset.preview && dataset.preview.length > 0 && (
                    <div className="dataset-quick-preview">
                      <h5>📋 Aperçu (5 premières lignes)</h5>
                      <div className="table-wrapper">
                        <table className="preview-table-compact">
                          <thead>
                            <tr>
                              {dataset.preview_columns.slice(0, 5).map((col, colIndex) => (
                                <th key={colIndex}>{col}</th>
                              ))}
                              {dataset.preview_columns.length > 5 && <th>...</th>}
                            </tr>
                          </thead>
                          <tbody>
                            {dataset.preview.map((row, rowIndex) => (
                              <tr key={rowIndex}>
                                {dataset.preview_columns.slice(0, 5).map((col, colIndex) => (
                                  <td key={colIndex} title={String(row[col] || '-')}>
                                    {row[col] !== null && row[col] !== undefined 
                                      ? String(row[col]).substring(0, 50) + (String(row[col]).length > 50 ? '...' : '')
                                      : '-'}
                                  </td>
                                ))}
                                {dataset.preview_columns.length > 5 && <td>...</td>}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                  
                  <a 
                    href={dataset.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="dataset-link-external"
                  >
                    Voir sur {dataset.source || 'le site'} →
                  </a>
                  
                  {!downloaded && (
                    <button 
                      className="download-btn"
                      onClick={() => handleDownload(dataset)}
                      disabled={isLoading}
                    >
                      {isLoading ? '⏳ Téléchargement...' : '📥 Télécharger le dataset complet'}
                    </button>
                  )}
                </div>
                
                {downloaded && (
                  <div className="dataset-preview">
                    <div className="preview-header">
                      <h5>Aperçu du dataset</h5>
                      <div className="preview-stats">
                        <span>Total: {downloaded.total_rows} lignes</span>
                        <span>Colonnes: {downloaded.columns.length}</span>
                        <span>Format: {downloaded.format.toUpperCase()}</span>
                      </div>
                    </div>
                    <div className="table-wrapper">
                      <table className="preview-table">
                        <thead>
                          <tr>
                            {downloaded.columns.map((col, colIndex) => (
                              <th key={colIndex}>{col}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {downloaded.preview.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                              {downloaded.columns.map((col, colIndex) => (
                                <td key={colIndex}>
                                  {row[col] !== null && row[col] !== undefined ? String(row[col]) : '-'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default QuantitativeAnalysis;
