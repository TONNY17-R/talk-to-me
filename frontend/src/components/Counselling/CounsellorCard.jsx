import React, { useState } from 'react';
import { Card } from '../Common/Card';
import './CounsellorCard.css';

export const CounsellorCard = ({ counsellor, onBook }) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <Card className="counsellor-card">
      <div className="counsellor-header">
        <div className="counsellor-avatar">
          {counsellor.avatarUrl ? (
            <img src={counsellor.avatarUrl} alt={counsellor.name} />
          ) : (
            <span>{counsellor.avatar}</span>
          )}
        </div>
        <div className="availability-badge">
          <span className="status-dot"></span>
          {counsellor.availability}
        </div>
      </div>

      <div className="counsellor-info">
        <h3>{counsellor.name}</h3>
        <p className="specialization">{counsellor.specialization}</p>

        <div className="rating-section">
          <span className="rating">⭐ {counsellor.rating}</span>
          <span className="reviews">({counsellor.reviews} reviews)</span>
        </div>

        <p className="bio-short">{counsellor.bio}</p>

        <div className="stats-grid">
          <div className="stat">
            <span className="stat-value">{counsellor.sessionsCompleted}</span>
            <span className="stat-label">Sessions</span>
          </div>
          <div className="stat">
            <span className="stat-value">{counsellor.successRate}</span>
            <span className="stat-label">Success</span>
          </div>
          <div className="stat">
            <span className="stat-value">{counsellor.price}</span>
            <span className="stat-label">Per Session</span>
          </div>
        </div>

        <div className="specialties-tags">
          {counsellor.specialties.map((spec) => (
            <span key={spec} className="specialty-tag">
              {spec}
            </span>
          ))}
        </div>

        {showDetails && (
          <div className="detailed-info">
            <p className="bio-full">{counsellor.bio_expanded}</p>
            <div className="details-section">
              <strong>Languages:</strong>
              <p>{counsellor.languages.join(', ')}</p>
            </div>
            <div className="details-section">
              <strong>Certifications:</strong>
              <p>{counsellor.certifications.join(', ')}</p>
            </div>
            <div className="details-section">
              <strong>Response Time:</strong>
              <p>{counsellor.responseTime}</p>
            </div>
          </div>
        )}
      </div>

      <div className="card-actions">
        <button
          className="details-button"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? '▼ Hide Details' : '▶ View Details'}
        </button>
        <button className="book-button" onClick={onBook}>
          Book Session ✓
        </button>
      </div>
    </Card>
  );
};
