import React, { useState } from 'react';
import { gad7Severity } from '../../utils/assessments';

export const GAD7Assessment = ({ onComplete }) => {
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState(null);

  const questions = [
    'Feeling nervous, anxious, or on edge',
    'Not being able to stop or control worrying',
    'Worrying too much about different things',
    'Trouble relaxing',
    'Being so restless that it is hard to sit still',
    'Becoming easily annoyed or irritable',
    'Feeling afraid as if something awful might happen',
  ];

  const totalAnswered = Object.keys(answers).length;
  const progress = Math.round((totalAnswered / questions.length) * 100);

  const handleAnswer = (questionIndex, score) => {
    setAnswers((prev) => ({ ...prev, [questionIndex]: score }));
    setError(null);
  };

  const handleSubmit = () => {
    if (totalAnswered !== questions.length) {
      setError('Please answer all questions before submitting.');
      return;
    }

    const total = Object.values(answers).reduce((a, b) => Number(a) + Number(b), 0);
    const severity = gad7Severity(total);
    onComplete({ assessment: 'GAD7', total, answers, severity });
  };

  return (
    <div className="assessment gad7-assessment">
      <h2>GAD-7 Anxiety Assessment</h2>

      <div className="assessment-progress">
        <div className="progress-bar" aria-hidden>
          <div className="progress-filled" style={{ width: `${progress}%` }} />
        </div>
        <div className="progress-label">{totalAnswered}/{questions.length} answered</div>
      </div>

      {questions.map((q, index) => (
        <div key={index} className="assessment-question">
          <p>{q}</p>
          <div className="answer-options" role="radiogroup" aria-label={`Question ${index + 1}`}>
            {[0, 1, 2, 3].map((score) => (
              <label key={score} className={`option ${answers[index] === score ? 'selected' : ''}`}>
                <input
                  type="radio"
                  name={`q${index}`}
                  value={score}
                  onChange={() => handleAnswer(index, score)}
                  checked={answers[index] === score}
                />
                <span className="option-text">{['Not at all', 'Several days', 'More than half the days', 'Nearly every day'][score]}</span>
              </label>
            ))}
          </div>
        </div>
      ))}

      {error && <div className="error-message">⚠️ {error}</div>}

      <div className="assessment-actions">
        <button className="btn-secondary" onClick={() => { setAnswers({}); setError(null); }}>
          Reset
        </button>
        <button className="btn-primary" onClick={handleSubmit}>
          Submit Assessment
        </button>
      </div>
    </div>
  );
};
