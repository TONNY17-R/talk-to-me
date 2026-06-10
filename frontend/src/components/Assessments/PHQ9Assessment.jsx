import React, { useState, useMemo } from 'react';
import { phq9Severity } from '../../utils/assessments';

export const PHQ9Assessment = ({ onComplete }) => {
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState(null);

  const questions = [
    'Little interest or pleasure in doing things',
    'Feeling down, depressed, or hopeless',
    'Trouble falling or staying asleep, or sleeping too much',
    'Feeling tired or having little energy',
    'Poor appetite or overeating',
    'Feeling bad about yourself — or that you are a failure or have let yourself or your family down',
    'Trouble concentrating on things, such as reading the newspaper or watching television',
    'Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving a lot more than usual',
    'Thoughts that you would be better off dead, or of hurting yourself in some way',
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
    const severity = phq9Severity(total);
    const result = { assessment: 'PHQ9', total, answers, severity };
    onComplete(result);
  };

  return (
    <div className="assessment phq9-assessment">
      <h2>PHQ-9 Depression Assessment</h2>
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
