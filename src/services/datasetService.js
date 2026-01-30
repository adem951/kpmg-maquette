/**
 * Service pour gérer les datasets via les APIs directes
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Recherche des datasets via les APIs officielles (data.gouv.fr, INSEE, etc.)
 * @param {string} query - Requête de recherche
 * @returns {Promise<Array>} Liste de datasets trouvés
 */
export const searchDatasets = async (query) => {
  try {
    console.log('🔍 Recherche datasets:', query);
    
    const response = await fetch(`${API_BASE_URL}/api/datasets/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Datasets trouvés:', data.count);
    
    return data.datasets || [];
  } catch (error) {
    console.error('❌ Erreur recherche datasets:', error);
    throw error;
  }
};

/**
 * Télécharge et parse un dataset spécifique
 * @param {string} url - URL du dataset
 * @returns {Promise<Object>} Dataset parsé avec preview
 */
export const downloadDataset = async (url) => {
  try {
    console.log('📥 Téléchargement dataset:', url);
    
    const response = await fetch(`${API_BASE_URL}/api/datasets/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Dataset téléchargé:', data.dataset.total_rows, 'lignes');
    
    return data.dataset;
  } catch (error) {
    console.error('❌ Erreur téléchargement dataset:', error);
    throw error;
  }
};

/**
 * Télécharge plusieurs datasets en parallèle
 * @param {Array<string>} urls - Liste d'URLs
 * @returns {Promise<Array>} Liste de datasets parsés
 */
export const downloadMultipleDatasets = async (urls) => {
  try {
    const promises = urls.map(url => downloadDataset(url));
    const results = await Promise.allSettled(promises);
    
    // Filtrer les succès
    const datasets = results
      .filter(result => result.status === 'fulfilled')
      .map(result => result.value);
    
    console.log(`✅ ${datasets.length}/${urls.length} datasets téléchargés`);
    return datasets;
  } catch (error) {
    console.error('❌ Erreur téléchargement multiple:', error);
    throw error;
  }
};
