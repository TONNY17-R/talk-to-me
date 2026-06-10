import React, { createContext, useState, useEffect } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userProfile, setUserProfile] = useState(null);
  const [assessmentHistory, setAssessmentHistory] = useState([]);

  const updateProfile = (profile) => {
    setUserProfile(profile);
  };

  const addAssessment = (assessment) => {
    setAssessmentHistory((prev) => [assessment, ...prev]);
  };

  return (
    <UserContext.Provider
      value={{
        userProfile,
        assessmentHistory,
        updateProfile,
        addAssessment,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
