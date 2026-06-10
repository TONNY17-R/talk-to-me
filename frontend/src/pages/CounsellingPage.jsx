import React, { useState, useEffect } from 'react';
import { CounsellorCard } from '../components/Counselling/CounsellorCard';
import { BookingModal } from '../components/Counselling/BookingModal';
import './CounsellingPage.css';

export const CounsellingPage = () => {
  const [counsellors, setCounsellors] = useState([]);
  const [filteredCounsellors, setFilteredCounsellors] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('all');
  const [selectedRating, setSelectedRating] = useState('all');
  const [selectedCounsellor, setSelectedCounsellor] = useState(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchCounsellors();
    fetchSessions();
  }, []);

  useEffect(() => {
    filterCounsellors();
  }, [counsellors, searchQuery, selectedSpecialty, selectedRating]);

  const fetchCounsellors = async () => {
    try {
      const response = await fetch('/api/counselling/counsellors');
      if (!response.ok) throw new Error('Failed to fetch counsellors');
      const data = await response.json();
      setCounsellors(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching counsellors:', error);
      setError(error.message);
      // Demo counsellors with enhanced data
      setCounsellors([
        {
          id: 1,
          name: 'Dr. Alice Johnson',
          avatarUrl: 'https://randomuser.me/api/portraits/women/44.jpg',
          avatar: '👩‍⚕️',
          specialization: 'Depression & Anxiety',
          bio: 'Licensed therapist with 10+ years of experience',
          rating: 4.9,
          reviews: 127,
          specialties: ['Depression', 'Anxiety', 'ADHD'],
          price: '$60/session',
          availability: 'Available Today',
          availableSlots: ['2:00 PM', '3:30 PM', '5:00 PM'],
          languages: ['English', 'Spanish'],
          certifications: ['LCSW', 'CBT Specialist'],
          sessionsCompleted: 450,
          successRate: '94%',
          responseTime: 'Usually responds in 1 hour',
          bio_expanded: 'Specializing in cognitive behavioral therapy for anxiety and depression. Compassionate, non-judgmental approach.',
        },
        {
          id: 2,
          name: 'Dr. Bob Smith',
          avatarUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
          avatar: '👨‍⚕️',
          specialization: 'PTSD & Trauma',
          bio: 'Trauma specialist with expertise in EMDR',
          rating: 4.8,
          reviews: 98,
          specialties: ['PTSD', 'Trauma', 'Grief'],
          price: '$75/session',
          availability: 'Available Tomorrow',
          availableSlots: ['10:00 AM', '11:30 AM', '2:00 PM'],
          languages: ['English', 'French'],
          certifications: ['EMDR Certified', 'PhD Psychology'],
          sessionsCompleted: 380,
          successRate: '91%',
          responseTime: 'Usually responds in 2 hours',
          bio_expanded: 'Expert in trauma recovery using evidence-based EMDR therapy. Supportive and client-centered approach.',
        },
        {
          id: 3,
          name: 'Dr. Carol White',
          avatarUrl: 'https://randomuser.me/api/portraits/women/47.jpg',
          avatar: '👩‍⚕️',
          specialization: 'Grief & Loss',
          bio: 'Compassionate counselor for bereavement support',
          rating: 4.7,
          reviews: 85,
          specialties: ['Grief', 'Loss', 'Life Transitions'],
          price: '$55/session',
          availability: 'Available in 1 hour',
          availableSlots: ['4:00 PM', '5:30 PM'],
          languages: ['English'],
          certifications: ['LCSW', 'Grief Counselor'],
          sessionsCompleted: 320,
          successRate: '92%',
          responseTime: 'Usually responds in 30 minutes',
          bio_expanded: 'Specializing in grief counseling and helping clients navigate loss with compassion and understanding.',
        },
        {
          id: 4,
          name: 'Dr. Emma Rodriguez',
          avatarUrl: 'https://randomuser.me/api/portraits/women/22.jpg',
          avatar: '👩‍⚕️',
          specialization: 'Relationships & Family',
          bio: 'Family therapist and relationship counselor',
          rating: 4.9,
          reviews: 142,
          specialties: ['Relationships', 'Family Issues', 'Couples Therapy'],
          price: '$65/session',
          availability: 'Available in 2 hours',
          availableSlots: ['3:00 PM', '4:30 PM'],
          languages: ['English', 'Spanish', 'Portuguese'],
          certifications: ['LMFT', 'Master Couples Therapist'],
          sessionsCompleted: 520,
          successRate: '95%',
          responseTime: 'Usually responds in 45 minutes',
          bio_expanded: 'Expert in couples therapy and family dynamics. Attachment-focused and solution-oriented approach.',
        },
      ]);
    }
  };

  const fetchSessions = async () => {
    try {
      const response = await fetch('/api/counselling/sessions');
      if (!response.ok) throw new Error('Failed to fetch sessions');
      const data = await response.json();
      setSessions(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching sessions:', error);
      // Demo sessions
      setSessions([
        {
          id: 1,
          counsellorName: 'Dr. Alice Johnson',
          date: '2026-02-12',
          time: '2:00 PM',
          type: 'Upcoming',
          duration: '60 min',
        },
        {
          id: 2,
          counsellorName: 'Dr. Bob Smith',
          date: '2026-02-05',
          time: '10:00 AM',
          type: 'Completed',
          duration: '60 min',
          notes: 'Good progress on PTSD coping strategies',
        },
      ]);
    }
  };

  const filterCounsellors = () => {
    let filtered = counsellors;

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(
        (c) =>
          c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          c.specialization.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Specialty filter
    if (selectedSpecialty !== 'all') {
      filtered = filtered.filter((c) =>
        c.specialties.includes(selectedSpecialty)
      );
    }

    // Rating filter
    if (selectedRating !== 'all') {
      const minRating = parseFloat(selectedRating);
      filtered = filtered.filter((c) => c.rating >= minRating);
    }

    setFilteredCounsellors(filtered);
  };

  const handleBookSession = (counsellor) => {
    setSelectedCounsellor(counsellor);
    setShowBookingModal(true);
  };

  const specialtyOptions = [
    'All Specialties',
    'Depression',
    'Anxiety',
    'PTSD',
    'Trauma',
    'Grief',
    'Relationships',
    'Family Issues',
  ];

  return (
    <div className="counselling-page">
      <div className="counselling-header">
        <h1>🏥 Professional Counselling Services</h1>
        <p>Connect with licensed therapists and counsellors</p>
      </div>

      {sessions.length > 0 && (
        <div className="upcoming-sessions">
          <h3>📅 Your Upcoming Sessions</h3>
          <div className="sessions-list">
            {sessions
              .filter((s) => s.type === 'Upcoming')
              .map((session) => (
                <div key={session.id} className="session-card">
                  <div className="session-info">
                    <strong>{session.counsellorName}</strong>
                    <p>{session.date} at {session.time}</p>
                    <span className="session-duration">{session.duration}</span>
                  </div>
                  <button className="join-button">Join Now 🎥</button>
                </div>
              ))}
          </div>
        </div>
      )}

      <div className="filters-section">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by name or specialization..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-controls">
          <select
            value={selectedSpecialty}
            onChange={(e) => setSelectedSpecialty(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Specialties</option>
            {specialtyOptions.slice(1).map((spec) => (
              <option key={spec} value={spec}>
                {spec}
              </option>
            ))}
          </select>

          <select
            value={selectedRating}
            onChange={(e) => setSelectedRating(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Ratings</option>
            <option value="4.5">4.5+ ⭐</option>
            <option value="4.7">4.7+ ⭐</option>
            <option value="4.9">4.9+ ⭐</option>
          </select>
        </div>
      </div>

      <div className="results-info">
        <p>Showing {filteredCounsellors.length} of {counsellors.length} counsellors</p>
      </div>

      <div className="counsellors-grid">
        {filteredCounsellors.map((counsellor) => (
          <CounsellorCard
            key={counsellor.id}
            counsellor={counsellor}
            onBook={() => handleBookSession(counsellor)}
          />
        ))}
      </div>

      {filteredCounsellors.length === 0 && (
        <div className="no-results">
          <p>No counsellors match your filters. Try adjusting your search.</p>
        </div>
      )}

      {showBookingModal && selectedCounsellor && (
        <BookingModal
          counsellor={selectedCounsellor}
          onClose={() => setShowBookingModal(false)}
          onConfirm={(bookingDetails) => {
            setSessions((prev) => [
              ...prev,
              {
                id: Date.now(),
                counsellorName: selectedCounsellor.name,
                date: bookingDetails.date,
                time: bookingDetails.time,
                type: 'Upcoming',
                duration: '60 min',
              },
            ]);
            setShowBookingModal(false);
          }}
        />
      )}
    </div>
  );
};
