import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css';

export const ChatInterface = ({ userId, sessionId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionActive, setSessionActive] = useState(true);
  const messagesEndRef = useRef(null);

  // Demo AI responses for fallback
  const demoResponses = [
    "I'm here to support you. What's on your mind?",
    "It sounds like you're dealing with a lot. Tell me more about what you're feeling.",
    "That's an important realization. How has that been affecting you?",
    "I understand. Many people experience similar feelings. Let's work through this together.",
    "You're being very brave in opening up. Have you considered speaking with a professional counselor?",
    "Your wellbeing matters. Would you like some suggestions for coping strategies?",
  ];

  const suggestedPrompts = [
    "😰 I'm feeling anxious",
    "😔 I'm feeling depressed",
    "😤 I'm stressed about work",
    "💔 I'm having relationship issues",
    "😴 I can't sleep",
    "🧘 I need relaxation tips",
  ];

  // Initialize with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMessage = {
        id: 'welcome',
        text: "👋 Hello! I'm your mental health support companion. I'm here to listen and help you navigate your feelings. How can I support you today?",
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getDemoResponse = () => {
    return demoResponses[Math.floor(Math.random() * demoResponses.length)];
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent',
    };

    const messageToSend = inputValue;
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Simulate AI typing delay
    await new Promise(resolve => setTimeout(resolve, 800));

    try {
      // API call to backend
      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageToSend,
          userId,
          sessionId,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = {
          id: Date.now() + 1,
          text: data.response || getDemoResponse(),
          sender: 'ai',
          timestamp: new Date(),
          sentiment: data.sentiment,
        };
        setMessages((prev) => [...prev, aiMessage]);
      } else {
        // Use demo response on API failure
        const aiMessage = {
          id: Date.now() + 1,
          text: getDemoResponse(),
          sender: 'ai',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, aiMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback demo response
      const aiMessage = {
        id: Date.now() + 1,
        text: getDemoResponse(),
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickPrompt = (prompt) => {
    const userMessage = {
      id: Date.now(),
      text: prompt,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent',
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        text: getDemoResponse(),
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleClearChat = () => {
    const welcomeMessage = {
      id: 'welcome',
      text: "👋 Chat cleared. How can I help you today?",
      sender: 'ai',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-title">
          <span className="status-dot"></span>
          Mental Health Support Chat
        </div>
        <button className="clear-chat-btn" onClick={handleClearChat} title="Clear chat">
          🔄
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-container message-${msg.sender}`}>
            <div className={`message-bubble message-${msg.sender}`}>
              <div className="message-content">{msg.text}</div>
              <div className="message-time">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-container message-ai">
            <div className="message-bubble message-ai">
              <div className="loading">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {messages.length <= 1 && !isLoading && (
        <div className="suggestions-section">
          <p className="suggestions-title">Quick prompts to get started:</p>
          <div className="suggestions-grid">
            {suggestedPrompts.map((prompt, idx) => (
              <button
                key={idx}
                className="suggestion-btn"
                onClick={() => handleQuickPrompt(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          type="text"
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Share your thoughts..."
          disabled={isLoading}
        />
        <button className="chat-send-button" type="submit" disabled={isLoading}>
          {isLoading ? '...' : '→'}
        </button>
      </form>
    </div>
  );
};
