import React from 'react';

export const MessageBubble = ({ message, sender }) => {
  return (
    <div className={`message-bubble message-bubble-${sender}`}>
      <div className="bubble-content">{message.text}</div>
      {message.sentiment && (
        <div className="sentiment-indicator" data-sentiment={message.sentiment}>
          {message.sentiment}
        </div>
      )}
    </div>
  );
};
