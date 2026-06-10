import React from 'react';

export const ResultsChart = ({ assessmentResults }) => {
  return (
    <div className="results-chart">
      <h3>Assessment Results</h3>
      <div className="chart-container">
        {assessmentResults?.map((result) => (
          <div key={result.id} className="result-item">
            <h4>{result.type}</h4>
            <div className="result-score">
              <div className="score-value">{result.score}</div>
              <div className="score-range">{result.interpretation}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
