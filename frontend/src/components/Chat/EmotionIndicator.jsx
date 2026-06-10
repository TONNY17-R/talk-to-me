import React from 'react';

export const EmotionIndicator = ({ sentiment, riskLevel }) => {
  const emotionMap = {
    very_negative: '😢',
    negative: '😟',
    neutral: '😐',
    positive: '🙂',
    very_positive: '😊',
  };

  const riskColorMap = {
    low: '#4caf50',
    medium: '#ff9800',
    high: '#f44336',
    critical: '#9c27b0',
  };

  return (
    <div className="emotion-indicator">
      <div className="emotion-emoji">{emotionMap[sentiment] || '😐'}</div>
      <div className="risk-level-indicator" style={{ backgroundColor: riskColorMap[riskLevel] }}>
        {riskLevel}
      </div>
    </div>
  );
};
