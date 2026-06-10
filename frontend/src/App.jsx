import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { ChatProvider } from './contexts/ChatContext';
import { UserProvider } from './contexts/UserContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { ToastProvider } from './contexts/ToastContext';
import { AppRoutes } from './routes';
import { BrowserRouter as Router } from 'react-router-dom';
import { Navbar } from './components/Common/Navbar';
import { Footer } from './components/Common/Footer';
import ErrorBoundary from './components/Common/ErrorBoundary';
import './styles/global.css';

function App() {
  return (
    <AuthProvider>
      <ChatProvider>
        <UserProvider>
          <ThemeProvider>
            <ToastProvider>
              <Router>
                <div className="app">
                  <Navbar />
                  <main className="main-content">
                    <ErrorBoundary>
                      <AppRoutes />
                    </ErrorBoundary>
                  </main>
                  <Footer />
                </div>
              </Router>
            </ToastProvider>
          </ThemeProvider>
        </UserProvider>
      </ChatProvider>
    </AuthProvider>
  );
}

export default App;
