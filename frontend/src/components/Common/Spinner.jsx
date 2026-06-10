import React from 'react';
import './Spinner.css';

export const Spinner = ({ size = 40, color = 'var(--primary)' }) => (
  <div
    className="spinner"
    style={{ width: size, height: size, borderColor: color }}
    aria-label="Loading"
  ></div>
);
