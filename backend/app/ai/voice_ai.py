import logging
import os
import tempfile

import pyttsx3
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from .tendo_ai import tendo_ai

logger = logging.getLogger(__name__)

class VoiceAIAssistant:
    """Voice-based AI assistant for Talk to Me"""
    
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engines
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Voice profiles for different languages
        self.voice_profiles = {
            'en': {'rate': 150, 'voice': 'english'},
            'lg': {'rate': 140, 'voice': 'english'},  # Fallback to English voice
            'sw': {'rate': 145, 'voice': 'english'}   # Fallback to English voice
        }
    
    def setup_tts(self):
        """Setup text-to-speech engine"""
        voices = self.tts_engine.getProperty('voices')
        # Try to find appropriate voices
        for voice in voices:
            if 'english' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        self.tts_engine.setProperty('rate', 150)  # Speech speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
    
    def speech_to_text(self, audio_data, language='en-US'):
        """Convert speech to text"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            logger.error("Speech recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
    
    def process_audio_file(self, audio_file_path, language='en-US'):
        """Process audio file and return text"""
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.speech_to_text(audio_data, language)
                return text
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            return None
    
    def text_to_speech(self, text, language='en', save_to_file=False):
        """Convert text to speech"""
        try:
            # Adjust TTS settings based on language
            voice_profile = self.voice_profiles.get(language, self.voice_profiles['en'])
            self.tts_engine.setProperty('rate', voice_profile['rate'])
            
            if save_to_file:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    temp_file = f.name
                
                # Use gTTS for better multilingual support
                tts = gTTS(text=text, lang=self.get_gtts_lang_code(language))
                tts.save(temp_file)
                return temp_file
            else:
                # Speak immediately
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return None
                
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            # Fallback to gTTS
            return self.gtts_fallback(text, language, save_to_file)
    
    def gtts_fallback(self, text, language='en', save_to_file=False):
        """Fallback using gTTS"""
        try:
            tts = gTTS(text=text, lang=self.get_gtts_lang_code(language))
            
            if save_to_file:
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    temp_file = f.name
                    tts.save(temp_file)
                    return temp_file
            else:
                # Play audio
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    temp_file = f.name
                    tts.save(temp_file)
                
                # Play the audio file
                audio = AudioSegment.from_mp3(temp_file)
                play(audio)
                os.unlink(temp_file)
                return None
                
        except Exception as e:
            logger.error(f"gTTS fallback error: {e}")
            return None
    
    def get_gtts_lang_code(self, language):
        """Get gTTS language code"""
        lang_map = {
            'en': 'en',
            'lg': 'en',  # Luganda not supported, fallback to English
            'sw': 'sw'   # Swahili
        }
        return lang_map.get(language, 'en')
    
    async def process_voice_message(self, audio_input, user_context):
        """Process voice message through AI pipeline"""
        # Step 1: Convert speech to text
        if isinstance(audio_input, str):  # Audio file path
            text = self.process_audio_file(audio_input)
        else:  # Audio data
            text = self.speech_to_text(audio_input)
        
        if not text:
            return {
                'error': 'Could not understand audio',
                'suggestions': ['Please speak clearly', 'Try typing instead']
            }
        
        # Step 2: Process text through Tendo AI
        chat_history = []  # Would get from database in production
        ai_response = await tendo_ai.generate_response(text, chat_history, user_context)
        
        # Step 3: Convert AI response to speech
        audio_response = self.text_to_speech(
            ai_response['response'],
            language=ai_response.get('language', 'en'),
            save_to_file=True
        )
        
        return {
            'transcript': text,
            'ai_response': ai_response,
            'audio_response_path': audio_response,
            'sentiment': ai_response['sentiment'],
            'risk_level': ai_response['risk_level']
        }
    
    def create_guided_meditation(self, duration=5, theme='calm', language='en'):
        """Create guided meditation audio"""
        scripts = {
            'calm': {
                'en': "Find a comfortable position. Close your eyes. Take a deep breath in... and slowly breathe out. Feel the tension leaving your body.",
                'lg': "Funa enkwaso ey'ekisa. Ggalawo amaso. Funa omukka ogw'amaanyi... olwo n'okussa omukka bulungi. Wulira okweraliikiriza okugenda mu mubiri gwo.",
                'sw': "Pata nafasi nyoofu. Fungua macho. Pumua ndani... kisha pumua polepole. Hisi mkazo ukiondoka mwilini mwako."
            },
            'sleep': {
                'en': "Imagine yourself in a peaceful place. The sounds are soft. Your body is heavy and relaxed. With each breath, you drift deeper into sleep.",
                'lg': "Ekirizibwa mu bifo by'emirembe. Amaloboozi g'ebigambo. Omubiri gwo gulina obunyiivu era gulina eky'okweyongera. Mu buli kukoppa, oyinza okwebaka obulungi.",
                'sw': "Jifikirie uko katika sehemu ya amani. Sauti ni laini. Mwili wako ni mzito na utulivu. Kwa kila pumzi, unaelekea usingizi mzito."
            }
        }
        
        script = scripts.get(theme, scripts['calm']).get(language, scripts['calm']['en'])
        
        # Generate audio
        audio_file = self.text_to_speech(script, language, save_to_file=True)
        
        return {
            'script': script,
            'audio_file': audio_file,
            'duration': duration,
            'theme': theme,
            'language': language
        }

# Global instance
voice_ai = VoiceAIAssistant()