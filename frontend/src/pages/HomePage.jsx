import React from 'react';
import { Link } from 'react-router-dom';
import '../pages/HomePage.css';

export const HomePage = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <span className="hero-pill">Support that feels human and local</span>
          <div className="hero-text-wrap">
            <p className="hero-kicker">A calmer, safer space for your mind and everyday wellbeing.</p>
            <h1>Welcome to Talk to Me</h1>
            <p className="hero-copy">
              Start with compassionate AI support, take a quick check-in, or connect with trusted counselling and resources in a few gentle steps.
            </p>
          </div>

          <div className="hero-badges" aria-label="Highlights">
            <span>24/7 guidance</span>
            <span>Local support</span>
            <span>Calm design</span>
          </div>
          <div className="hero-actions">
            <Link to="/chat" className="cta-button">Start Chatting</Link>
            <Link to="/assessment" className="secondary-button">Take an Assessment</Link>
          </div>
        </div>
      </section>

      <section className="support-strip" aria-label="Why people use Talk to Me">
        <article className="support-card">
          <h3>Private & judgement-free</h3>
          <p>Get support in a space designed to feel calm, respectful, and easy to use.</p>
        </article>
        <article className="support-card">
          <h3>Simple next steps</h3>
          <p>Move from a quick check-in to chat, counselling, or tailored resources in a few taps.</p>
        </article>
        <article className="support-card">
          <h3>Built for Uganda</h3>
          <p>Support that reflects local needs, practical guidance, and welcoming care.</p>
        </article>
      </section>

      <section className="features">
        <h2>Our Services</h2>
        <div className="features-grid">
          <div className="feature">
            <span className="feature-icon">💬</span>
            <h3>AI Chat Support</h3>
            <p>24/7 support from our AI counsellor for quick guidance, reassurance, and reflection.</p>
          </div>
          <div className="feature">
            <span className="feature-icon">🧪</span>
            <h3>Assessments</h3>
            <p>Take PHQ-9 and GAD-7 assessments to better understand your wellbeing.</p>
          </div>
          <div className="feature">
            <span className="feature-icon">🤝</span>
            <h3>Professional Counselling</h3>
            <p>Connect with trained counsellors for deeper, human support when you need it.</p>
          </div>
          <div className="feature">
            <span className="feature-icon">📚</span>
            <h3>Resources</h3>
            <p>Access articles, videos, and exercises to support your daily wellbeing journey.</p>
          </div>
        </div>
      </section>
    </div>
  );
};
