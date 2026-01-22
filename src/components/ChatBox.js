import React, { useState, useRef, useEffect } from 'react';
import './ChatBox.css';
import { analyzeChatInput } from '../services/apiService';

const ChatBox = ({ onSendMessage }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Bonjour ! Je suis votre assistant d'analyse de marché KPMG. Comment puis-je vous aider aujourd'hui ?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (inputValue.trim() === '') return;

    const query = inputValue;
    
    // Ajouter le message de l'utilisateur
    const userMessage = {
      id: messages.length + 1,
      text: query,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages([...messages, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Message de traitement
      const processingMessage = {
        id: messages.length + 2,
        text: "🔍 Analyse en cours avec l'IA...",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, processingMessage]);

      // Appel à l'API pour analyser l'entrée utilisateur
      const response = await analyzeChatInput(query);
      
      setIsTyping(false);
      
      // Vérifier si c'est un refus d'intention (détection basée sur le contenu)
      const isIntentionRefused = response.includes("**Demande non compatible avec l'analyse de marché**");
      
      // Passer la réponse au composant parent pour l'affichage dans QualitativeAnalysis
      onSendMessage(query, response);
      
      // Message de confirmation adapté selon si l'intention est refusée ou acceptée
      let completionMessage;
      if (isIntentionRefused) {
        completionMessage = {
          id: messages.length + 3,
          text: `⚠️ Votre demande ne correspond pas à une analyse de marché. Veuillez reformuler en précisant le marché ou secteur à analyser. Consultez les suggestions dans la section "Données Qualitatives".`,
          sender: 'bot',
          timestamp: new Date()
        };
      } else {
        completionMessage = {
          id: messages.length + 3,
          text: `✅ Votre analyse est prête ! Consultez les résultats dans la section "Données Qualitatives".`,
          sender: 'bot',
          timestamp: new Date()
        };
      }
      setMessages(prev => [...prev, completionMessage]);
      
    } catch (error) {
      setIsTyping(false);
      
      // Message d'erreur
      const errorMessage = {
        id: messages.length + 3,
        text: "❌ Une erreur est survenue lors de l'analyse. Veuillez réessayer.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      
      console.error('Erreur lors de l\'analyse:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  };

  const quickQuestions = [
    "Analyse du marché des véhicules électriques",
    "Marché du e-commerce en France",
    "Tendances du marché actuel"
  ];

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="chatbox">
      <div className="chatbox-header">
        <div className="header-content">
          <div className="bot-avatar">🤖</div>
          <div className="header-text">
            <h3>Assistant IA - Analyse de Marché</h3>
            <span className="status">En ligne</span>
          </div>
        </div>
      </div>

      <div className="chatbox-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-content">
              <p>{message.text}</p>
              <span className="message-time">{formatTime(message.timestamp)}</span>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message bot">
            <div className="message-content typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {messages.length <= 1 && (
        <div className="quick-questions">
          <p className="quick-questions-title">Questions rapides :</p>
          {quickQuestions.map((question, index) => (
            <button
              key={index}
              className="quick-question-btn"
              onClick={() => handleQuickQuestion(question)}
            >
              {question}
            </button>
          ))}
        </div>
      )}

      <div className="chatbox-input">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Décrivez votre besoin d'analyse de marché..."
          rows="2"
        />
        <button onClick={handleSend} disabled={inputValue.trim() === ''}>
          <span>Envoyer</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
