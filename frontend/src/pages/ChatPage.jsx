import React, { useContext } from 'react';
import { ChatInterface } from '../components/Chat/ChatInterface';
import { ChatContext } from '../contexts/ChatContext';
import './ChatPage.css';

export const ChatPage = () => {
  const { chatSession } = useContext(ChatContext);

  return (
    <div className="chat-page">
      <ChatInterface
        userId={chatSession?.userId}
        sessionId={chatSession?.sessionId}
      />
    </div>
  );
};
