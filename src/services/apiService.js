/**
 * Service pour les appels API vers le backend
 * Gère les recherches Tavily et les analyses de marché
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Effectue une recherche générale (contexte, tendances, acteurs)
 */
export const searchGeneral = async (query, maxResults = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/search/general`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        mode: 'general',
        max_results: maxResults,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Erreur lors de la recherche générale:', error);
    throw error;
  }
};

/**
 * Effectue une recherche de données quantitatives
 */
export const searchData = async (query, maxResults = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/search/data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        mode: 'data',
        max_results: maxResults,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Erreur lors de la recherche de données:', error);
    throw error;
  }
};

/**
 * Analyse l'entrée utilisateur depuis la ChatBox avec le LLM
 */
export const analyzeChatInput = async (message) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Erreur lors de l\'analyse du message:', error);
    throw error;
  }
};

/**
 * Génère une analyse de marché complète
 */
export const generateAnalysis = async (query, includeWebSearch = true) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        include_web_search: includeWebSearch,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data.analysis;
  } catch (error) {
    console.error('Erreur lors de la génération de l\'analyse:', error);
    throw error;
  }
};

/**
 * Récupère les données de marché depuis la BDD
 */
export const getMarketData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/market-data`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    throw error;
  }
};

/**
 * Sauvegarde les données de marché dans la BDD
 */
export const saveMarketData = async (marketData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/market-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(marketData),
    });

    if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erreur lors de la sauvegarde des données:', error);
    throw error;
  }
};

/**
 * Vérifie l'état de santé de l'API
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      return { status: 'offline' };
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API inaccessible:', error);
    return { status: 'offline' };
  }
};

export default {
  searchGeneral,
  searchData,
  analyzeChatInput,
  generateAnalysis,
  getMarketData,
  saveMarketData,
  checkHealth,
};
