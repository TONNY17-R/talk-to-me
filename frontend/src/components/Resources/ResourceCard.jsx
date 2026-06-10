import React from 'react';
import { Card } from '../Common/Card';

export const ResourceCard = ({ resource }) => {
  const handleViewResource = () => {
    if (resource.url) {
      window.open(resource.url, '_blank');
    }
  };

  return (
    <Card className="resource-card">
      <div className="resource-image">
        {resource.imageUrl ? (
          <img src={resource.imageUrl} alt={resource.title} />
        ) : (
          <span>{resource.icon || '📚'}</span>
        )}
      </div>
      <div className="resource-content">
        <div className="resource-type">{resource.type}</div>
        <h3>{resource.title}</h3>
        {resource.channel && <p className="channel-name">Channel: {resource.channel}</p>}
        <p>{resource.description}</p>
        {resource.tags && (
          <div className="tags">
            {resource.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
      <div className="resource-footer">
        {resource.subscribers && <span className="subscribers">{resource.subscribers}</span>}
        <button className="view-button" onClick={handleViewResource}>
          {resource.type === 'youtube' ? 'Watch on YouTube' : 'View Resource'}
        </button>
      </div>
    </Card>
  );
};
