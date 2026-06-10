import React from 'react';
import './Footer.css';

export const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-flag-stripes" aria-hidden="true">
        <span className="stripe stripe-black" />
        <span className="stripe stripe-yellow" />
        <span className="stripe stripe-red" />
      </div>
      <div className="footer-content">
        <div className="footer-section">
          <h4>About Talk to Me</h4>
          <p>Mental health support platform for Uganda</p>
        </div>
        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/privacy">Privacy Policy</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>Emergency</h4>
          <p>Crisis Support: +256 70 700 6833</p>
          <p>
            WhatsApp Support: <a href="https://wa.me/256707006833?text=Hello%20Talk%20to%20Me%20Support%2C%20I%20need%20help" target="_blank" rel="noopener noreferrer">
              +256 70 700 6833
            </a>
          </p>
          <p>
            Join our WhatsApp group: <a href="https://chat.whatsapp.com/your-group-code" target="_blank" rel="noopener noreferrer">
              Join the community
            </a>
          </p>
          <p>SMWANGA DELIN SMITH</p>
        </div>
      </div>
      <p className="footer-copyright">&copy; 2026 Talk to Me. All rights reserved.</p>
    </footer>
  );
};
