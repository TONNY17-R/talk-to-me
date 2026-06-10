import React, { useState, useEffect } from 'react';

export const ProgressTracker = ({ userId }) => {
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    fetchProgress();
  }, [userId]);

  const fetchProgress = async () => {
    try {
      const response = await fetch(`/api/assessment/progress/${userId}`);
      const data = await response.json();
      setProgress(data);
    } catch (error) {
      console.error('Error fetching progress:', error);
    }
  };

  if (!progress) return <div>Loading...</div>;

  return (
    <div className="progress-tracker">
      <h3>Your Progress</h3>
      <div className="progress-items">
        {progress.map((item) => (
          <div key={item.id} className="progress-item">
            <h4>{item.assessmentType}</h4>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${item.percentage}%` }} />
            </div>
            <p>{item.date}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
