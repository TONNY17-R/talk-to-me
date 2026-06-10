import React from 'react';

export const EmergencyAlert = ({ isVisible, onClose }) => {
  if (!isVisible) return null;

  return (
    <div className="emergency-alert">
      <div className="alert-content">
        <h2>Crisis Support</h2>
        <p>If you are in immediate danger, please contact emergency services.</p>
        <p>National Crisis Hotline: 0800 XXXXX</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};
