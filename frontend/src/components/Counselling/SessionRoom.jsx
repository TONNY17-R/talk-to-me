import React from 'react';

export const SessionRoom = ({ sessionId, isActive }) => {
  return (
    <div className="session-room">
      <h2>Counselling Session</h2>
      <div className="video-container">
        <video id="remote-video" />
        <video id="local-video" muted />
      </div>
      <div className="session-controls">
        <button className="mute-btn">Mute</button>
        <button className="video-btn">Video Off</button>
        <button className="end-call-btn">End Session</button>
      </div>
    </div>
  );
};
