import React from 'react';

export const AnalyticsChart = ({ data }) => {
  return (
    <div className="analytics-chart">
      <h2>Analytics</h2>
      <div className="chart-container">
        {/* Chart implementation would go here */}
        <p>Chart data: {JSON.stringify(data)}</p>
      </div>
    </div>
  );
};
