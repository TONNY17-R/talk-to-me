import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export const ProfilePage = () => {
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user]);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`/api/user/profile/${user.id}`);
      const data = await response.json();
      setProfile(data);
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      {profile && (
        <div className="profile-content">
          <div className="profile-info">
            <h2>{profile.name}</h2>
            <p>{profile.email}</p>
            <p>Joined: {profile.joinedDate}</p>
          </div>
          {!isEditing && (
            <button onClick={() => setIsEditing(true)}>Edit Profile</button>
          )}
        </div>
      )}
    </div>
  );
};
