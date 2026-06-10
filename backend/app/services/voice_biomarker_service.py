"""
Voice Biomarker & Audio Analysis Service
Analyzes voice characteristics for emotion detection, depression/anxiety indicators, and suicidality risk
"""

import librosa
import numpy as np
from typing import Dict, Tuple, Optional
import logging
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler
import requests
from config import Config
import json

logger = logging.getLogger(__name__)


class VoiceBiomarkerService:
    """Analyzes voice recordings for mental health biomarkers"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.scaler = StandardScaler()
        self.emotion_model = None
        self.depression_detector = None
        self.suicide_risk_model = None
        self.load_models()
    
    def load_models(self):
        """Load pre-trained speech analysis models"""
        try:
            # Try to load models from saved weights
            logger.info("Loading voice analysis models...")
            # Placeholder for actual model loading
        except Exception as e:
            logger.warning(f"Could not load voice models: {e}")
    
    def analyze_voice_recording(
        self,
        audio_path: str,
        user_id: int,
        language: str = 'en'
    ) -> Dict:
        """
        Comprehensive voice analysis for mental health indicators
        
        Args:
            audio_path: Path or URL to audio file
            user_id: User ID
            language: Language code (en, lg, sw)
        
        Returns:
            Dictionary with emotion, depression, anxiety, and suicide risk indicators
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract comprehensive features
            features = self._extract_voice_features(y, sr)
            
            # Perform multiple analyses
            emotion_analysis = self._detect_emotion(features)
            depression_indicators = self._analyze_depression_indicators(features)
            anxiety_indicators = self._analyze_anxiety_indicators(features)
            suicide_risk = self._analyze_suicide_risk(features)
            speech_pattern = self._analyze_speech_patterns(y, sr)
            
            return {
                'user_id': user_id,
                'audio_duration_seconds': len(y) / sr,
                'language': language,
                'emotion_analysis': emotion_analysis,
                'depression_indicators': depression_indicators,
                'anxiety_indicators': anxiety_indicators,
                'suicide_risk_assessment': suicide_risk,
                'speech_characteristics': speech_pattern,
                'overall_mental_state': self._determine_overall_state(
                    emotion_analysis,
                    depression_indicators,
                    anxiety_indicators,
                    suicide_risk
                ),
                'recommendation': self._generate_voice_recommendation(
                    emotion_analysis,
                    suicide_risk
                ),
                'transcription_needed': False,
                'features_extracted': True
            }
        except Exception as e:
            logger.error(f"Error analyzing voice recording: {e}")
            return {
                'user_id': user_id,
                'error': str(e),
                'features_extracted': False
            }
    
    def detect_vocal_emotion(self, audio_path: str) -> Dict:
        """
        Detect emotional state from voice
        
        Returns:
            Emotion classification and confidence
        """
        try:
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            features = self._extract_voice_features(y, sr)
            
            emotion_scores = {
                'neutral': self._calculate_emotion_score(features, 'neutral'),
                'happy': self._calculate_emotion_score(features, 'happy'),
                'sad': self._calculate_emotion_score(features, 'sad'),
                'anxious': self._calculate_emotion_score(features, 'anxious'),
                'angry': self._calculate_emotion_score(features, 'angry'),
                'depressed': self._calculate_emotion_score(features, 'depressed'),
            }
            
            # Normalize scores
            total = sum(emotion_scores.values())
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
            
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            confidence = emotion_scores[primary_emotion]
            
            return {
                'primary_emotion': primary_emotion,
                'confidence': confidence,
                'emotion_distribution': emotion_scores,
                'is_positive': primary_emotion in ['happy', 'neutral']
            }
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return {'error': str(e)}
    
    def analyze_speech_rate_and_patterns(self, audio_path: str) -> Dict:
        """
        Analyze speech rate, pitch, intensity, and other vocal patterns
        
        Returns:
            Detailed speech pattern metrics
        """
        try:
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract speech features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            # Calculate speech rate (approximate from zero crossing rate)
            speech_rate_wpm = self._estimate_speech_rate(y, sr)
            
            # Detect pauses
            pause_times = self._detect_pauses(y, sr)
            
            # Pitch analysis
            pitch_contour = self._extract_pitch_contour(y, sr)
            
            return {
                'speech_rate_wpm': speech_rate_wpm,
                'average_pitch_hz': np.mean(pitch_contour) if pitch_contour else 0,
                'pitch_variance': np.std(pitch_contour) if pitch_contour else 0,
                'pitch_range': (np.min(pitch_contour), np.max(pitch_contour)) if pitch_contour else (0, 0),
                'voice_intensity': float(np.mean(np.abs(y))),
                'pause_count': len(pause_times),
                'pause_duration_avg': np.mean(pause_times) if pause_times else 0,
                'stutter_frequency': self._detect_stutter(y, sr),
                'vocal_fry_detected': self._detect_vocal_fry(y, sr),
                'articulation_clarity': self._measure_articulation(y, sr),
                'spectral_characteristics': {
                    'centroid_mean': float(np.mean(spectral_centroid)),
                    'centroid_std': float(np.std(spectral_centroid)),
                },
                'zero_crossing_rate_mean': float(np.mean(zero_crossing_rate)),
            }
        except Exception as e:
            logger.error(f"Error analyzing speech patterns: {e}")
            return {'error': str(e)}
    
    def track_voice_trend(
        self,
        user_id: int,
        recent_recordings: list,
        week_starting: str
    ) -> Dict:
        """
        Track voice pattern trends over time (weekly)
        
        Returns:
            Trend analysis showing improvement or decline
        """
        try:
            trend_data = {
                'speech_rates': [],
                'average_pitches': [],
                'voice_intensities': [],
                'pause_frequencies': [],
                'emotions': []
            }
            
            for recording in recent_recordings[-7:]:  # Last 7 days
                analysis = self.analyze_speech_rate_and_patterns(recording['path'])
                emotion = self.detect_vocal_emotion(recording['path'])
                
                trend_data['speech_rates'].append(analysis.get('speech_rate_wpm', 0))
                trend_data['average_pitches'].append(analysis.get('average_pitch_hz', 0))
                trend_data['voice_intensities'].append(analysis.get('voice_intensity', 0))
                trend_data['pause_frequencies'].append(analysis.get('pause_count', 0))
                trend_data['emotions'].append(emotion.get('primary_emotion', 'neutral'))
            
            # Calculate trends
            if len(trend_data['speech_rates']) > 1:
                speech_trend = trend_data['speech_rates'][-1] - trend_data['speech_rates'][0]
                pitch_trend = trend_data['average_pitches'][-1] - trend_data['average_pitches'][0]
                intensity_trend = trend_data['voice_intensities'][-1] - trend_data['voice_intensities'][0]
            else:
                speech_trend = pitch_trend = intensity_trend = 0
            
            return {
                'user_id': user_id,
                'week_starting': week_starting,
                'avg_speech_rate': np.mean(trend_data['speech_rates']),
                'avg_pitch': np.mean(trend_data['average_pitches']),
                'avg_intensity': np.mean(trend_data['voice_intensities']),
                'total_pause_time': sum(trend_data['pause_frequencies']),
                'average_utterance_length': np.mean(trend_data['speech_rates']) * 0.25,  # Rough estimate
                'lexical_diversity': self._estimate_lexical_diversity(recent_recordings),
                'trend_direction': 'improving' if (speech_trend > 10 and intensity_trend > 0.01) else (
                    'declining' if (speech_trend < -10 or intensity_trend < -0.01) else 'stable'
                ),
                'dominant_emotion': max(set(trend_data['emotions']), key=trend_data['emotions'].count),
                'emotional_consistency': 1.0 - (len(set(trend_data['emotions'])) / len(trend_data['emotions'])) if trend_data['emotions'] else 0.5,
            }
        except Exception as e:
            logger.error(f"Error tracking voice trend: {e}")
            return {'user_id': user_id, 'error': str(e)}
    
    def transcribe_voice_to_text(self, audio_path: str, language: str = 'en') -> Dict:
        """
        Transcribe voice recording to text using speech-to-text API
        
        Returns:
            Transcribed text and confidence score
        """
        try:
            # Use a speech-to-text API (e.g., Google Cloud Speech-to-Text or Whisper)
            # This is a placeholder - implement with your chosen provider
            
            # For Whisper API (simple implementation):
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            try:
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                
                transcription = recognizer.recognize_google(audio, language=language)
                
                return {
                    'transcription': transcription,
                    'confidence': 0.85,  # Placeholder
                    'language': language,
                    'character_count': len(transcription),
                    'word_count': len(transcription.split()),
                }
            except sr.UnknownValueError:
                return {'error': 'Could not understand audio'}
            except sr.RequestError as e:
                return {'error': f'Speech recognition error: {e}'}
                
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return {'error': str(e)}
    
    # Helper methods
    
    def _extract_voice_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract comprehensive voice features"""
        features = {}
        
        # MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfcc, axis=1)
        features['mfcc_std'] = np.std(mfcc, axis=1)
        
        # Spectral features
        features['spectral_centroid'] = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y)
        
        # Temporal features
        features['rms_energy'] = librosa.feature.rms(y=y)
        features['tempogram'] = librosa.feature.tempogram(y=y, sr=sr)
        
        return features
    
    def _detect_emotion(self, features: Dict) -> Dict:
        """Detect emotional state from features"""
        # Simplified emotion detection based on feature characteristics
        mfcc_variance = np.mean(features['mfcc_std'])
        spectral_cent = np.mean(features['spectral_centroid'])
        energy = np.mean(features['rms_energy'])
        
        emotion_score = {
            'neutral': 0.5,
            'happy': energy * 1.2 if spectral_cent > 2000 else energy,
            'sad': (1 - energy) * 0.9,
            'anxious': mfcc_variance * 1.5,
            'angry': energy * spectral_cent / 1000,
            'depressed': (1 - energy) * (1 - spectral_cent / 5000),
        }
        
        # Normalize
        total = sum(emotion_score.values())
        emotion_score = {k: v/total for k, v in emotion_score.items()}
        
        primary = max(emotion_score.items(), key=lambda x: x[1])[0]
        
        return {
            'detected_emotion': primary,
            'confidence': emotion_score[primary],
            'all_emotions': emotion_score
        }
    
    def _analyze_depression_indicators(self, features: Dict) -> Dict:
        """Analyze indicators of depression"""
        # Depression typically associated with: low energy, monotone voice, slower speech
        energy = np.mean(features['rms_energy'])
        spectral_variety = np.std(features['spectral_centroid'])
        
        depression_score = 0
        if energy < 0.1:
            depression_score += 0.4
        if spectral_variety < 500:
            depression_score += 0.3
        
        return {
            'depression_likelihood': min(1.0, depression_score),
            'energy_level': float(energy),
            'vocal_monotony': 1 - (float(spectral_variety) / 3000),
            'indicators': [
                'low_energy' if energy < 0.1 else None,
                'monotone_voice' if spectral_variety < 500 else None,
            ]
        }
    
    def _analyze_anxiety_indicators(self, features: Dict) -> Dict:
        """Analyze indicators of anxiety"""
        # Anxiety typically associated with: high pitch, high energy, variable pace
        energy = np.mean(features['rms_energy'])
        spectral_cent = np.mean(features['spectral_centroid'])
        
        anxiety_score = 0
        if energy > 0.2:
            anxiety_score += 0.3
        if spectral_cent > 3000:
            anxiety_score += 0.3
        
        return {
            'anxiety_likelihood': min(1.0, anxiety_score),
            'energy_level': float(energy),
            'pitch_elevation': float(spectral_cent) / 5000,
            'indicators': [
                'elevated_pitch' if spectral_cent > 3000 else None,
                'high_energy' if energy > 0.2 else None,
            ]
        }
    
    def _analyze_suicide_risk(self, features: Dict) -> Dict:
        """Analyze suicidality risk from voice characteristics"""
        # Suicide risk indicators: hopelessness (low energy, slow speech, restricted range)
        energy = np.mean(features['rms_energy'])
        spectral_range = np.max(features['spectral_centroid']) - np.min(features['spectral_centroid'])
        
        risk_score = 0
        if energy < 0.08:
            risk_score += 0.3
        if spectral_range < 1000:
            risk_score += 0.3
        
        return {
            'suicidality_risk_score': min(1.0, risk_score),
            'risk_level': 'critical' if risk_score > 0.7 else ('high' if risk_score > 0.4 else 'low'),
            'indicators': [
                'hopelessness_markers' if energy < 0.08 else None,
                'restricted_emotional_range' if spectral_range < 1000 else None,
            ],
            'recommendation': 'Immediate crisis intervention' if risk_score > 0.7 else 'Monitor closely'
        }
    
    def _analyze_speech_patterns(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze detailed speech patterns"""
        return {
            'speech_rate': self._estimate_speech_rate(y, sr),
            'pause_count': len(self._detect_pauses(y, sr)),
            'stutter_frequency': self._detect_stutter(y, sr),
            'vocal_fry': self._detect_vocal_fry(y, sr),
        }
    
    def _estimate_speech_rate(self, y: np.ndarray, sr: int) -> float:
        """Estimate speech rate in words per minute"""
        # Simplified: use zero crossing rate and energy
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        rms = np.mean(librosa.feature.rms(y=y))
        
        # Rough estimate: WPM
        estimated_wpm = (zcr * 1000) + (rms * 100)
        return max(50, min(300, float(estimated_wpm)))  # Clamp between realistic values
    
    def _detect_pauses(self, y: np.ndarray, sr: int) -> list:
        """Detect and measure pauses in speech"""
        # Use energy to detect pauses
        energy = np.sqrt(np.convolve(y**2, np.ones(sr//10)/sr*10))
        threshold = np.mean(energy) * 0.1
        
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i, e in enumerate(energy):
            if e < threshold:
                if not in_pause:
                    pause_start = i
                    in_pause = True
            else:
                if in_pause:
                    pauses.append((i - pause_start) / sr)
                    in_pause = False
        
        return pauses
    
    def _extract_pitch_contour(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract pitch contour using PYIN algorithm"""
        try:
            f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=500, sr=sr)
            return f0[~np.isnan(f0)]
        except:
            return np.array([])
    
    def _detect_stutter(self, y: np.ndarray, sr: int) -> float:
        """Detect stuttering frequency"""
        # Simplified: detect rapid energy fluctuations
        rms = librosa.feature.rms(y=y)[0]
        differences = np.diff(rms)
        
        stutter_count = np.sum(np.abs(differences) > np.mean(np.abs(differences)) * 2)
        return float(stutter_count / len(rms))
    
    def _detect_vocal_fry(self, y: np.ndarray, sr: int) -> bool:
        """Detect vocal fry (creaky voice)"""
        # Vocal fry has very low frequency content
        S = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr, n_fft=S.shape[0]*2)
        low_freq_content = np.sum(S[freqs < 100])
        total_content = np.sum(S)
        
        return (low_freq_content / total_content) > 0.3
    
    def _measure_articulation(self, y: np.ndarray, sr: int) -> float:
        """Measure articulation clarity (0-1)"""
        # Articulation measured by spectral flux
        S = np.abs(librosa.stft(y))
        spectral_flux = np.sqrt(np.sum(np.diff(S, axis=1)**2, axis=0))
        
        # Normalized clarity score
        clarity = np.mean(spectral_flux) / (np.std(spectral_flux) + 1e-6)
        return float(min(1.0, clarity / 10))
    
    def _estimate_lexical_diversity(self, recordings: list) -> float:
        """Estimate lexical diversity from recordings"""
        # Placeholder: in practice, would use transcriptions
        return 0.7
    
    def _calculate_emotion_score(self, features: Dict, emotion: str) -> float:
        """Calculate emotion score based on features"""
        # Simplified scoring function
        base_score = 0.5
        
        energy = np.mean(features['rms_energy'])
        spectral_cent = np.mean(features['spectral_centroid'])
        
        if emotion == 'happy':
            return base_score + (energy * 0.3) + ((spectral_cent / 5000) * 0.2)
        elif emotion == 'sad':
            return base_score + ((1 - energy) * 0.3) + ((1 - spectral_cent / 5000) * 0.2)
        elif emotion == 'anxious':
            return base_score + (energy * 0.2) + (np.std(features['spectral_centroid']) / 1000 * 0.3)
        elif emotion == 'angry':
            return base_score + (energy * 0.4)
        elif emotion == 'depressed':
            return base_score + ((1 - energy) * 0.4)
        else:  # neutral
            return base_score
    
    def _determine_overall_state(self, emotion, depression, anxiety, suicide) -> str:
        """Determine overall mental state from multiple indicators"""
        if suicide['suicidality_risk_score'] > 0.6:
            return 'critical_suicidal_risk'
        elif depression['depression_likelihood'] > 0.6:
            return 'moderate_to_severe_depression'
        elif anxiety['anxiety_likelihood'] > 0.6:
            return 'moderate_to_severe_anxiety'
        elif emotion['detected_emotion'] == 'happy':
            return 'positive_affect'
        elif emotion['detected_emotion'] == 'sad':
            return 'depressed_mood'
        else:
            return 'neutral_mental_state'
    
    def _generate_voice_recommendation(self, emotion, suicide) -> str:
        """Generate recommendation based on voice analysis"""
        if suicide['suicidality_risk_score'] > 0.6:
            return 'URGENT: Immediate crisis intervention required. Contact emergency services.'
        elif emotion['detected_emotion'] in ['sad', 'depressed'] and emotion['confidence'] > 0.7:
            return 'Consider increased therapy frequency and psychiatric evaluation.'
        elif emotion['detected_emotion'] == 'anxious' and emotion['confidence'] > 0.7:
            return 'Recommend anxiety management techniques and possibly medication review.'
        else:
            return 'Continue with current treatment plan. Monitor for changes.'
