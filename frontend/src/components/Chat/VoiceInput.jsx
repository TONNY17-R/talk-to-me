import React, { useState } from 'react';

export const VoiceInput = ({ onTranscript, isListening }) => {
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setIsRecording(true);
      // Implementation for voice recording
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    // Implementation for stopping recording
  };

  return (
    <button
      onClick={isRecording ? stopRecording : startRecording}
      className={`voice-input-btn ${isRecording ? 'recording' : ''}`}
    >
      {isRecording ? 'Stop Recording' : 'Start Voice Input'}
    </button>
  );
};
