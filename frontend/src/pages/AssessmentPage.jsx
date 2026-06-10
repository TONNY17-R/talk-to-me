import React, { useState } from 'react';
import { PHQ9Assessment } from '../components/Assessments/PHQ9Assessment';
import { GAD7Assessment } from '../components/Assessments/GAD7Assessment';
import { saveAssessmentToLocal } from '../utils/assessments';
import './AssessmentPage.css';

export const AssessmentPage = () => {
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [results, setResults] = useState(null);
  const [saving, setSaving] = useState(false);

  const handleAssessmentComplete = (result) => {
    setResults(result);
  };

  const handleSave = async () => {
    if (!results) return;
    setSaving(true);
    try {
      // Try backend save (stub). If it fails, fallback to localStorage
      const res = await fetch('/api/assessments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(results),
      });

      if (!res.ok) {
        // fallback
        saveAssessmentToLocal(results);
      }
    } catch (err) {
      saveAssessmentToLocal(results);
    }
    setSaving(false);
    alert('Result saved (local fallback used if API unavailable).');
  };

  return (
    <div className="assessment-page">
      <h1>Mental Health Assessments</h1>

      {!selectedAssessment && !results && (
        <div className="assessment-selection">
          <button onClick={() => setSelectedAssessment('phq9')}>
            PHQ-9 Assessment
          </button>
          <button onClick={() => setSelectedAssessment('gad7')}>
            GAD-7 Assessment
          </button>
        </div>
      )}

      {selectedAssessment === 'phq9' && (
        <PHQ9Assessment onComplete={handleAssessmentComplete} />
      )}

      {selectedAssessment === 'gad7' && (
        <GAD7Assessment onComplete={handleAssessmentComplete} />
      )}

      {results && (
        <div className="assessment-results">
          <h2>Results</h2>
          <p>
            <strong>{results.assessment}</strong> score: <span className="result-score">{results.total}</span>
          </p>
          {results.severity && (
            <div className="result-level" style={{ borderLeft: `6px solid ${results.severity.color}`, paddingLeft: '12px' }}>
              <h3>{results.severity.level}</h3>
              <p>{results.severity.interpretation}</p>
            </div>
          )}

          <div className="result-actions">
            <button onClick={() => { setSelectedAssessment(null); setResults(null); }} className="btn-secondary">
              Take Another Assessment
            </button>
            <button onClick={handleSave} className="btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save Result'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
