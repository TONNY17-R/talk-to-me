import React from 'react';

export const VideoPlayer = ({ videoUrl, title }) => {
  return (
    <div className="video-player">
      <video controls width="100%">
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <h3>{title}</h3>
    </div>
  );
};
