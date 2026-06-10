import React, { createContext, useState, useCallback } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [chatSession, setChatSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionHistory, setSessionHistory] = useState([]);

  const startSession = useCallback((userId) => {
    const newSession = {
      userId,
      sessionId: Date.now().toString(),
      startTime: new Date(),
      status: 'active',
    };
    setChatSession(newSession);
    setMessages([]);
    return newSession;
  }, []);

  const addMessage = useCallback((message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  const addMessages = useCallback((messagesArray) => {
    setMessages((prev) => [...prev, ...messagesArray]);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const endSession = useCallback(() => {
    if (chatSession) {
      const completedSession = {
        ...chatSession,
        endTime: new Date(),
        messageCount: messages.length,
        status: 'completed',
      };
      setSessionHistory((prev) => [...prev, completedSession]);
    }
    setChatSession(null);
    setMessages([]);
  }, [chatSession, messages.length]);

  const getSessionStats = useCallback(() => {
    return {
      totalSessions: sessionHistory.length,
      totalMessages: messages.length,
      currentSession: chatSession ? {
        duration: new Date() - chatSession.startTime,
        messageCount: messages.length,
      } : null,
    };
  }, [sessionHistory, messages.length, chatSession]);

  return (
    <ChatContext.Provider
      value={{
        chatSession,
        messages,
        isTyping,
        sessionHistory,
        startSession,
        addMessage,
        addMessages,
        clearMessages,
        endSession,
        setIsTyping,
        getSessionStats,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};
