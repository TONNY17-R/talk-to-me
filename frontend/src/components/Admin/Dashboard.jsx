import React, { useState, useEffect } from 'react';

export const Dashboard = ({ adminUser }) => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/admin/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <div className="stats-grid">
        {stats && (
          <>
            <div className="stat-card">
              <h3>Total Users</h3>
              <p className="stat-value">{stats.totalUsers}</p>
            </div>
            <div className="stat-card">
              <h3>Active Sessions</h3>
              <p className="stat-value">{stats.activeSessions}</p>
            </div>
            <div className="stat-card">
              <h3>Crisis Alerts</h3>
              <p className="stat-value">{stats.crisisAlerts}</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
