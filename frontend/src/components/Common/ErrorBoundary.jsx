import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, info: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    this.setState({ error, info });
    // Also log to console for debugging
    // eslint-disable-next-line no-console
    console.error('ErrorBoundary caught an error', error, info);
  }

  render() {
    const { hasError, error, info } = this.state;
    if (hasError) {
      return (
        <div style={{ padding: 20 }}>
          <h2>Something went wrong rendering the app</h2>
          <pre style={{ whiteSpace: 'pre-wrap', background: '#f6f6f6', padding: 12, borderRadius: 6 }}>
            {String(error && error.toString())}
            {info && info.componentStack}
          </pre>
          <p>Check the browser console and report the error text.</p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
