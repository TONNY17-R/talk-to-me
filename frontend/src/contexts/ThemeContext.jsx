import React, { createContext, useState, useEffect } from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('darkMode', next);
      } catch {}
      return next;
    });
  };

  // synchronize body class for CSS variables
  useEffect(() => {
    document.body.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  const theme = {
    isDarkMode,
    primaryColor: isDarkMode ? '#8ee7e8' : '#3ec9c0',
    secondaryColor: isDarkMode ? '#5b9fb0' : '#1f5a79',
    backgroundColor: isDarkMode ? '#18252b' : '#f4fbfd',
    textColor: isDarkMode ? '#eff7f8' : '#22343c',
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, isDarkMode }}>
      {children}
    </ThemeContext.Provider>
  );
};
