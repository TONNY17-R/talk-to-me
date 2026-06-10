import React, { useState, useEffect } from 'react';
import { ResourceCard } from '../components/Resources/ResourceCard';
import './ResourcesPage.css';

export const ResourcesPage = () => {
  const [resources, setResources] = useState([]);
  const [filter, setFilter] = useState('all');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResources();
  }, [filter]);

  const getDemoResources = () => {
    const allDemoResources = [
      // YouTube Channels
      {
        id: 1,
        title: 'Therapy in a Nutshell',
        channel: 'Therapy in a Nutshell',
        type: 'youtube',
        icon: '🎬',
        imageUrl: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=800&q=80',
        subscribers: '1.2M subscribers',
        description: 'Psychology-based mental health tips and therapy concepts explained clearly.',
        tags: ['Psychology', 'Mental Health', 'Education'],
        url: 'https://www.youtube.com/@TherapyInaNutshell'
      },
      {
        id: 2,
        title: 'The Honest Guys',
        channel: 'The Honest Guys',
        type: 'youtube',
        icon: '🧘',
        imageUrl: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=800&q=80',
        subscribers: '2.8M subscribers',
        description: 'Guided meditations, breathing exercises, and relaxation techniques for anxiety and sleep.',
        tags: ['Meditation', 'Relaxation', 'Sleep'],
        url: 'https://www.youtube.com/@TheHonestGuys'
      },
      {
        id: 3,
        title: 'BetterHelp',
        channel: 'BetterHelp',
        type: 'youtube',
        icon: '💬',
        imageUrl: 'https://images.unsplash.com/photo-1516515429572-18a451ac43ce?auto=format&fit=crop&w=800&q=80',
        subscribers: '900K subscribers',
        description: 'Professional mental health advice and counseling tips from licensed therapists.',
        tags: ['Counseling', 'Therapy', 'Professional Help'],
        url: 'https://www.youtube.com/@BetterHelp'
      },
      {
        id: 4,
        title: 'Actual Advice Genetics',
        channel: 'Actual Advice Genetics',
        type: 'youtube',
        icon: '🧬',
        imageUrl: 'https://images.unsplash.com/photo-1505750436836-3f60cb2bd36b?auto=format&fit=crop&w=800&q=80',
        subscribers: '500K subscribers',
        description: 'Mental health science, depression help, and practical wellness strategies.',
        tags: ['Science', 'Depression', 'Wellness'],
        url: 'https://www.youtube.com/@actualadvicegenetics'
      },
      {
        id: 5,
        title: 'Meditation Made Simple',
        channel: 'Meditation Made Simple',
        type: 'youtube',
        icon: '🕉️',
        imageUrl: 'https://images.unsplash.com/photo-1511988617509-a57c8a288659?auto=format&fit=crop&w=800&q=80',
        subscribers: '800K subscribers',
        description: 'Beginner-friendly meditation and mindfulness practices for stress relief.',
        tags: ['Mindfulness', 'Stress Relief', 'Beginner'],
        url: 'https://www.youtube.com/@MeditationMadeSimple'
      },
      {
        id: 6,
        title: 'Psychology Today',
        channel: 'Psychology Today',
        type: 'youtube',
        icon: '📖',
        imageUrl: 'https://images.unsplash.com/photo-1532074205216-d0e1f03a7d5d?auto=format&fit=crop&w=800&q=80',
        subscribers: '600K subscribers',
        description: 'Expert mental health information, therapy insights, and psychological research.',
        tags: ['Psychology', 'Research', 'Education'],
        url: 'https://www.youtube.com/@PsychologyToday'
      },
      // Articles
      {
        id: 7,
        title: 'Understanding Depression',
        type: 'article',
        icon: '📚',
        imageUrl: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=800&q=80',
        description: 'A comprehensive guide to understanding depression, its causes, and treatment options.',
        tags: ['Depression', 'Mental Health', 'Education'],
        url: '#'
      },
      {
        id: 8,
        title: 'Anxiety Management Techniques',
        type: 'article',
        icon: '📝',
        imageUrl: 'https://images.unsplash.com/photo-1496318447583-f524534e9ce1?auto=format&fit=crop&w=800&q=80',
        description: 'Practical techniques and strategies to manage anxiety in daily life.',
        tags: ['Anxiety', 'Coping', 'Self-Help'],
        url: '#'
      },
      // Exercises
      {
        id: 9,
        title: '5-Minute Breathing Exercise',
        type: 'exercise',
        icon: '🫁',
        imageUrl: 'https://images.unsplash.com/photo-1517423440428-a5a00ad493e8?auto=format&fit=crop&w=800&q=80',
        description: 'A quick breathing exercise to calm your mind and reduce stress.',
        tags: ['Breathing', 'Stress Relief', 'Quick'],
        url: '#'
      },
      {
        id: 10,
        title: 'Progressive Muscle Relaxation',
        type: 'exercise',
        icon: '💪',
        imageUrl: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80',
        description: 'Release physical tension and anxiety through guided muscle relaxation.',
        tags: ['Relaxation', 'Tension', 'Body'],
        url: '#'
      }
    ];

    // Filter based on current filter state
    if (filter === 'all') {
      return allDemoResources;
    }
    return allDemoResources.filter((resource) => resource.type === filter);
  };

  const fetchResources = async () => {
    try {
      const response = await fetch(`/api/resources?type=${filter}`);
      if (!response.ok) throw new Error('Failed to fetch resources');
      const data = await response.json();
      setResources(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching resources:', error);
      setError(error.message);
      // Set filtered demo resources
      setResources(getDemoResources());
    }
  };

  return (
    <div className="resources-page">
      <h1>Mental Health Resources</h1>
      <div className="resources-filter">
        <button className={`filter-button ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>All</button>
        <button className={`filter-button ${filter === 'youtube' ? 'active' : ''}`} onClick={() => setFilter('youtube')}>YouTube Channels</button>
        <button className={`filter-button ${filter === 'article' ? 'active' : ''}`} onClick={() => setFilter('article')}>Articles</button>
        <button className={`filter-button ${filter === 'exercise' ? 'active' : ''}`} onClick={() => setFilter('exercise')}>Exercises</button>
      </div>
      <div className="resources-grid">
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </div>
    </div>
  );
};
