import React, { useState, useEffect } from 'react';

export const CrisisAlerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('/api/admin/crisis-alerts');
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  return (
    <div className="crisis-alerts">
      <h2>Crisis Alerts</h2>
      <div className="alerts-list">
        {alerts.map((alert) => (
          <div key={alert.id} className={`alert-item alert-${alert.level}`}>
            <h3>{alert.user}</h3>
            <p>{alert.message}</p>
            <p className="alert-time">{alert.timestamp}</p>
            <button>Take Action</button>
          </div>
        ))}
      </div>
    </div>
  );
};
