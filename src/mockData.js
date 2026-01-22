// Fonction pour obtenir une analyse en fonction de la requête
export const getAnalysis = (query) => {
  const lowerQuery = query.toLowerCase();
  
  // Recherche par mots-clés
  if (lowerQuery.includes('véhicule') || lowerQuery.includes('électrique') || lowerQuery.includes('voiture')) {
    return mockAnalyses["marché des véhicules électriques"];
  }
  
  if (lowerQuery.includes('e-commerce') || lowerQuery.includes('commerce en ligne') || lowerQuery.includes('vente en ligne')) {
    return mockAnalyses["marché du e-commerce en france"];
  }
  
  // Retourne l'analyse par défaut si aucune correspondance
  return mockAnalyses["default"];
};

// Messages prédéfinis du chatbot
export const chatbotResponses = {
  greeting: "Bonjour ! Je suis votre assistant d'analyse de marché KPMG. Comment puis-je vous aider aujourd'hui ?",
  processing: "Je traite votre demande et prépare l'analyse...",
  completed: "Votre analyse de marché est prête ! Consultez les résultats ci-dessous.",
  help: "Vous pouvez me demander une analyse sur différents marchés comme : véhicules électriques, e-commerce, santé digitale, etc."
};
