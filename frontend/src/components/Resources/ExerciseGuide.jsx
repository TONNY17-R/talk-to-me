import React from 'react';

export const ExerciseGuide = ({ exercise }) => {
  return (
    <div className="exercise-guide">
      <h2>{exercise.name}</h2>
      <p className="duration">Duration: {exercise.duration}</p>
      <div className="instructions">
        <h3>Instructions:</h3>
        <ol>
          {exercise.steps?.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      </div>
      {exercise.videoUrl && (
        <video controls width="100%" src={exercise.videoUrl} />
      )}
    </div>
  );
};
