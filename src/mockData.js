// Données fictives simulant les réponses de l'IA
export const mockAnalyses = {
  "marché des véhicules électriques": {
    qualitative: {
      title: "Analyse Qualitative - Marché des Véhicules Électriques",
      sections: [
        {
          subtitle: "Vue d'ensemble du marché",
          content: "Le marché des véhicules électriques connaît une croissance exponentielle avec une adoption accélérée dans les principaux marchés mondiaux. Les facteurs clés incluent les réglementations environnementales strictes, les incitations gouvernementales et la sensibilisation croissante aux enjeux climatiques."
        },
        {
          subtitle: "Tendances principales",
          content: "• Transition vers l'électrification totale d'ici 2030-2035 dans plusieurs pays européens\n• Amélioration constante de l'autonomie des batteries (moyenne de 400-500 km)\n• Réduction des coûts de production grâce aux économies d'échelle\n• Développement rapide de l'infrastructure de recharge"
        },
        {
          subtitle: "Acteurs principaux",
          content: "Tesla domine le marché avec 20% de part, suivi par BYD (15%), Volkswagen Group (12%), et les constructeurs traditionnels qui investissent massivement dans l'électrification. Les nouveaux entrants comme Rivian et Lucid Motors apportent de l'innovation."
        },
        {
          subtitle: "Opportunités",
          content: "• Forte demande dans les segments premium et SUV électriques\n• Marché des batteries et recyclage en pleine expansion\n• Services de recharge et maintenance spécialisée\n• Technologies de conduite autonome intégrées aux VE"
        },
        {
          subtitle: "Défis et risques",
          content: "• Dépendance aux matières premières rares (lithium, cobalt)\n• Infrastructure de recharge encore insuffisante dans certaines régions\n• Coût initial élevé malgré les aides gouvernementales\n• Concurrence intense et guerre des prix"
        }
      ],
      recommendation: "Le marché des véhicules électriques présente des opportunités exceptionnelles pour les investisseurs et entreprises. Nous recommandons une approche stratégique focalisée sur l'innovation technologique, les partenariats stratégiques et l'expansion dans les marchés émergents."
    },
    quantitative: {
      marketSize: {
        labels: ['2021', '2022', '2023', '2024', '2025 (proj.)'],
        data: [4.6, 7.8, 10.5, 14.2, 18.9],
        unit: 'millions d\'unités'
      },
      marketShare: {
        labels: ['Tesla', 'BYD', 'Volkswagen', 'GM', 'Autres'],
        data: [20, 15, 12, 8, 45],
        colors: ['#00d4ff', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0']
      },
      regionalGrowth: {
        labels: ['Chine', 'Europe', 'Amérique du Nord', 'Asie-Pacifique', 'Reste du monde'],
        data: [45, 28, 15, 8, 4],
        growth: [12.5, 18.2, 15.8, 22.3, 10.5]
      },
      priceEvolution: {
        labels: ['2020', '2021', '2022', '2023', '2024'],
        avgPrice: [55000, 52000, 48000, 45000, 42000],
        batteryCost: [140, 132, 120, 110, 100]
      }
    }
  },
  "marché du e-commerce en france": {
    qualitative: {
      title: "Analyse Qualitative - E-commerce en France",
      sections: [
        {
          subtitle: "Contexte du marché",
          content: "Le marché français du e-commerce a atteint 147 milliards d'euros en 2023, avec une croissance de 11% par rapport à 2022. La pandémie a accéléré la digitalisation des habitudes d'achat, créant une transformation structurelle durable."
        },
        {
          subtitle: "Comportements consommateurs",
          content: "• 89% des Français ont effectué un achat en ligne en 2023\n• Panier moyen: 65€\n• Mobile représente 42% des transactions\n• Préférence pour la livraison gratuite et rapide\n• Importance croissante des avis clients et du service après-vente"
        },
        {
          subtitle: "Secteurs porteurs",
          content: "Mode et accessoires (24%), électronique et high-tech (18%), produits culturels (12%), alimentation et épicerie en ligne (en forte croissance +35% en 2023), beauté et cosmétiques, ameublement et décoration."
        },
        {
          subtitle: "Innovations technologiques",
          content: "• Personnalisation par IA et machine learning\n• Réalité augmentée pour l'essayage virtuel\n• Chatbots et assistants virtuels\n• Paiements simplifiés et sécurisés (Apple Pay, Google Pay)\n• Social commerce via Instagram et TikTok"
        },
        {
          subtitle: "Enjeux stratégiques",
          content: "Développement durable et e-commerce responsable, optimisation de la logistique (last mile), omnicanalité et expérience client unifiée, protection des données personnelles (RGPD), concurrence des marketplaces internationales."
        }
      ],
      recommendation: "Le marché du e-commerce français offre des perspectives solides. Les opportunités se concentrent sur l'expérience client personnalisée, le mobile-first, et l'intégration de solutions durables. Les PME doivent adopter une stratégie omnicanale pour rester compétitives."
    },
    quantitative: {
      marketSize: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024 (proj.)'],
        data: [103, 112, 129, 137, 147, 161],
        unit: 'milliards €'
      },
      marketShare: {
        labels: ['Amazon', 'Cdiscount', 'Fnac', 'Veepee', 'Autres'],
        data: [28, 12, 8, 6, 46],
        colors: ['#ff9900', '#00a650', '#f39200', '#7c00d4', '#95a5a6']
      },
      regionalGrowth: {
        labels: ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Autres régions'],
        data: [32, 15, 11, 9, 33],
        growth: [10.5, 12.8, 13.2, 14.5, 11.8]
      },
      priceEvolution: {
        labels: ['2019', '2020', '2021', '2022', '2023'],
        avgPrice: [58, 62, 63, 64, 65],
        transactions: [1.78, 1.81, 2.05, 2.14, 2.26]
      }
    }
  },
  "default": {
    qualitative: {
      title: "Analyse de Marché Générique",
      sections: [
        {
          subtitle: "Aperçu",
          content: "Cette analyse fournit un cadre général pour évaluer un marché. Pour une analyse plus précise, veuillez spécifier le secteur d'activité qui vous intéresse."
        },
        {
          subtitle: "Méthodologie",
          content: "Notre approche combine l'analyse PESTEL, les 5 forces de Porter, l'étude de la chaîne de valeur et l'analyse de la concurrence pour fournir une vision complète du marché."
        },
        {
          subtitle: "Points clés",
          content: "• Analyse de la taille et de la croissance du marché\n• Identification des segments porteurs\n• Cartographie concurrentielle\n• Tendances et innovations\n• Opportunités et menaces"
        }
      ],
      recommendation: "Pour obtenir une analyse détaillée, merci de préciser votre secteur d'activité (par exemple: véhicules électriques, e-commerce, santé digitale, etc.)"
    },
    quantitative: {
      marketSize: {
        labels: ['2020', '2021', '2022', '2023', '2024'],
        data: [100, 115, 132, 148, 165],
        unit: 'milliards €'
      },
      marketShare: {
        labels: ['Leader', 'Challenger 1', 'Challenger 2', 'Spécialistes', 'Autres'],
        data: [35, 20, 15, 18, 12],
        colors: ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#95a5a6']
      },
      regionalGrowth: {
        labels: ['Europe', 'Amérique du Nord', 'Asie', 'Amérique Latine', 'Autres'],
        data: [35, 30, 25, 7, 3],
        growth: [8.5, 10.2, 15.8, 12.3, 6.5]
      },
      priceEvolution: {
        labels: ['2020', '2021', '2022', '2023', '2024'],
        avgPrice: [100, 102, 105, 108, 110],
        volume: [1000, 1128, 1257, 1370, 1500]
      }
    }
  }
};

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
