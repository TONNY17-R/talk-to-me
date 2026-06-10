import openai
import json
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import datetime
from config import Config
import logging
from typing import Dict, List, Optional, Tuple
import re

logger = logging.getLogger(__name__)

class TendoAI:
    """Advanced AI Mental Health Assistant for Ugandan Youth"""
    
    def __init__(self):
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Load sentiment analysis model
        logger.info("Loading sentiment analysis model...")
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Load crisis detection model
        logger.info("Loading crisis detection model...")
        try:
            self.crisis_tokenizer = AutoTokenizer.from_pretrained(
                "mental-health-models/crisis-detector",
                cache_dir="ml_models/"
            )
            self.crisis_model = AutoModelForSequenceClassification.from_pretrained(
                "mental-health-models/crisis-detector",
                cache_dir="ml_models/"
            )
        except:
            logger.warning("Crisis detection model not found, using rule-based fallback")
            self.crisis_model = None
        
        # Load Luganda NLP model
        logger.info("Loading Luganda NLP model...")
        self.luganda_detector = self.load_luganda_model()
        
        # Crisis keywords in multiple languages
        self.crisis_keywords = {
            'en': [
                'suicide', 'kill myself', 'end it all', 'want to die',
                'self-harm', 'cutting', 'hopeless', 'worthless',
                'can\'t go on', 'ending my life', 'no reason to live'
            ],
            'lg': [
                'okwetta', 'nkwete', 'okufa', 'sigula muntu',
                'sinnaba kweyagira', 'nsinziira', 'nta kintu kyolina'
            ],
            'sw': [
                'kujiua', 'kujinyonga', 'kukata tamaa',
                'sina matumaini', 'napenda kufa'
            ]
        }
        
        # Cultural context for Uganda
        self.cultural_context = {
            'common_stressors': [
                'academic pressure', 'unemployment', 'family expectations',
                'financial stress', 'relationship issues', 'peer pressure',
                'social media comparison', 'future uncertainty'
            ],
            'local_resources': {
                'helpline': '0800-123-456',
                'butabika': 'Butabika National Referral Hospital',
                'strongminds': 'StrongMinds Uganda',
                'mentality': 'Mentality Uganda'
            },
            'culturally_appropriate_responses': [
                "It's okay to not be okay. In our culture, we're taught to be strong, "
                "but even the strongest trees bend in the storm.",
                "Remember the saying: 'Obuzibu bwe bubaawo, ekitiibwa ky'omuntu tekirina mwoto.' "
                "(When problems come, a person's dignity doesn't diminish).",
                "Let's approach this like we do back home - one step at a time, "
                "with the support of our community."
            ]
        }
        
        # Response templates
        self.response_templates = self.load_response_templates()
        
    def load_luganda_model(self):
        """Load Luganda language model"""
        try:
            # Try to load custom Luganda model
            from transformers import AutoModelForTokenClassification
            model = AutoModelForTokenClassification.from_pretrained(
                "afri-bert/afriberta_large",
                cache_dir="ml_models/"
            )
            return model
        except:
            # Fallback to language detection
            from langdetect import detect
            return detect
    
    def load_response_templates(self) -> Dict:
        """Load response templates for different scenarios"""
        return {
            'greeting': {
                'en': "Hello! I'm Tendo, your mental health companion. How are you feeling today?",
                'lg': "Nkulamusizza! Nze Tendo, omukwano gwo mu by'ebyo by'okweraliikiriza. Oli otya leero?",
                'sw': "Habari! Mimi ni Tendo, mshirika wako wa afya ya akili. Unajisikiaje leo?"
            },
            'crisis_high': {
                'en': "I'm really concerned about what you're sharing. Please call the emergency helpline at 0800-123-456 right now. I'll stay with you while you get help.",
                'lg': "Nnina okweraliikiriza ku by'olina okunnyonnyola. Saba okuyita ennamba ya pulojekiti 0800-123-456 kaakati. Nja kubeera n'owe buli lwe wona obuyambi.",
                'sw': "Nina wasiwasi kuhusu unachosema. Tafadhali piga simu ya dharura 0800-123-456 sasa hivi. Nitakaa nawe mpaka upate usaidizi."
            },
            'follow_up': {
                'en': "How has that been affecting your daily life?",
                'lg': "Kino kiba kiitandika okukutwala mu bulamu bwo buli lunaku otya?",
                'sw': "Hii imekuathiri vipi maisha yako ya kila siku?"
            },
            'resource_suggestion': {
                'en': "Based on what you've shared, you might find this helpful: ",
                'lg': "Ku lw'ebyo wona okunnyonnyola, kino kiyinza okukuyamba: ",
                'sw': "Kulingana na ulichoshiriki, hii inaweza kukusaidia: "
            }
        }
    
    async def generate_response(self, user_message: str, chat_history: List[Dict], 
                              user_context: Dict) -> Dict:
        """Generate AI response with advanced features"""
        
        # Detect language
        language = self.detect_language(user_message)
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(user_message)
        
        # Check for crisis
        risk_level, crisis_indicators = self.assess_risk(user_message, language)
        
        # Update user context
        user_context.update({
            'current_sentiment': sentiment,
            'risk_level': risk_level,
            'language': language
        })
        
        # Generate response based on risk level
        if risk_level in ['high', 'critical']:
            response = self.generate_crisis_response(user_message, risk_level, language)
            escalation_needed = True
        else:
            response = await self.generate_general_response(
                user_message, chat_history, user_context, language
            )
            escalation_needed = False
        
        # Extract entities and topics
        entities = self.extract_entities(user_message)
        topics = self.identify_topics(user_message)
        
        # Generate personalized recommendations
        recommendations = self.generate_recommendations(
            user_context, sentiment, topics, language
        )
        
        # Generate follow-up questions
        follow_ups = self.generate_followup_questions(topics, language)
        
        return {
            'response': response,
            'sentiment': sentiment,
            'risk_level': risk_level,
            'crisis_indicators': crisis_indicators,
            'language': language,
            'entities': entities,
            'topics': topics,
            'recommendations': recommendations,
            'follow_up_questions': follow_ups,
            'escalation_needed': escalation_needed,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of the text"""
        if self.luganda_detector and hasattr(self.luganda_detector, 'predict'):
            # Use ML model for detection
            try:
                prediction = self.luganda_detector.predict([text])
                return prediction[0]
            except:
                pass
        
        # Fallback to rule-based detection
        text_lower = text.lower()
        
        # Luganda indicators
        luganda_words = ['mwana', 'nyabo', 'ssebo', 'kale', 'webale', 'oli', 'otyano']
        if any(word in text_lower for word in luganda_words):
            return 'lg'
        
        # Swahili indicators
        swahili_words = ['habari', 'asante', 'sawa', 'pole', 'mambo', 'vipi']
        if any(word in text_lower for word in swahili_words):
            return 'sw'
        
        # Default to English
        return 'en'
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment with emotion detection"""
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            label = result['label']
            score = float(result['score'])
            
            # Map to our emotion categories
            emotion_map = {
                'positive': 'happy',
                'negative': 'sad',
                'neutral': 'neutral'
            }
            
            return {
                'label': emotion_map.get(label, label),
                'score': score,
                'emotion': self.detect_emotion(text, label, score)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                'label': 'neutral',
                'score': 0.5,
                'emotion': 'neutral'
            }
    
    def detect_emotion(self, text: str, sentiment: str, score: float) -> str:
        """Detect specific emotion from text"""
        emotion_keywords = {
            'anxiety': ['worried', 'anxious', 'nervous', 'scared', 'afraid'],
            'anger': ['angry', 'mad', 'frustrated', 'annoyed', 'irritated'],
            'sadness': ['sad', 'depressed', 'lonely', 'empty', 'hopeless'],
            'stress': ['stressed', 'overwhelmed', 'pressure', 'burned out'],
            'hope': ['hopeful', 'optimistic', 'better', 'improving']
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return 'neutral'
    
    def assess_risk(self, text: str, language: str = 'en') -> Tuple[str, List[str]]:
        """Assess risk level and extract crisis indicators"""
        text_lower = text.lower()
        crisis_indicators = []
        
        # Check keywords
        keywords = self.crisis_keywords.get(language, self.crisis_keywords['en'])
        for keyword in keywords:
            if keyword in text_lower:
                crisis_indicators.append(keyword)
        
        # Use ML model if available
        if self.crisis_model:
            try:
                inputs = self.crisis_tokenizer(
                    text, 
                    return_tensors="pt", 
                    truncation=True, 
                    max_length=512
                )
                with torch.no_grad():
                    outputs = self.crisis_model(**inputs)
                risk_score = torch.sigmoid(outputs.logits[0][0]).item()
            except:
                risk_score = len(crisis_indicators) * 0.2
        else:
            risk_score = len(crisis_indicators) * 0.2
        
        # Determine risk level
        if risk_score > 0.8 or len(crisis_indicators) >= 3:
            return 'critical', crisis_indicators
        elif risk_score > 0.6 or len(crisis_indicators) >= 2:
            return 'high', crisis_indicators
        elif risk_score > 0.4 or len(crisis_indicators) >= 1:
            return 'medium', crisis_indicators
        else:
            return 'low', crisis_indicators
    
    async def generate_general_response(self, message: str, history: List[Dict], 
                                      context: Dict, language: str) -> str:
        """Generate empathetic AI response"""
        
        # Build system prompt with cultural context
        system_prompt = f"""You are Tendo, a mental health support assistant for Ugandan youth.
        You are empathetic, culturally aware, and provide supportive responses.
        
        User Context:
        - Age: {context.get('age', 'young adult')}
        - Location: {context.get('location', 'Uganda')}
        - Language: {language}
        - Current mood: {context.get('current_mood', 'neutral')}
        - Previous sentiment: {context.get('current_sentiment', {}).get('label', 'neutral')}
        
        Cultural Guidelines:
        1. Use appropriate proverbs and sayings for the culture
        2. Be respectful of family and community values
        3. Acknowledge common stressors in Ugandan youth context
        4. Suggest locally available resources
        
        Response Guidelines:
        1. Be warm and supportive, not clinical
        2. Ask open-ended questions to encourage sharing
        3. Validate feelings without judgment
        4. Suggest small, manageable steps
        5. If professional help is needed, suggest gently
        
        Previous conversation context:
        {self.format_chat_history(history[-3:])}
        
        Respond in {language} if possible, otherwise use English."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            *history[-5:],
            {"role": "user", "content": message}
        ]
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4" if context.get('risk_level') == 'medium' else "gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=200,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )
            
            response_text = response.choices[0].message.content
            
            # Post-process response for cultural appropriateness
            response_text = self.culturally_adjust_response(response_text, language)
            
            return response_text
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to template responses
            return self.response_templates['follow_up'].get(language, 
                   self.response_templates['follow_up']['en'])
    
    def generate_crisis_response(self, message: str, risk_level: str, language: str) -> str:
        """Generate crisis response with emergency resources"""
        
        # Get emergency resources based on location
        location = "Uganda"
        emergency_resources = self.get_emergency_resources(location)
        
        # Build crisis response
        crisis_template = self.response_templates['crisis_high'].get(
            language, self.response_templates['crisis_high']['en']
        )
        
        response = crisis_template + "\n\n"
        
        # Add specific resources
        for resource in emergency_resources[:3]:
            response += f"• {resource['name']}: {resource['contact']}\n"
        
        # Add reassurance
        reassurance = {
            'en': "\nYou are not alone. Help is available and people care about you.",
            'lg': "\nToli waka. Obuyambi buliwo era abantu bakweraliikiriza ku ggwe.",
            'sw': "\nWewe si peke yako. Usaidizi upo na watu wanakujali."
        }
        
        response += reassurance.get(language, reassurance['en'])
        
        return response
    
    def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities (people, places, issues) from text"""
        entities = []
        
        # Simple rule-based entity extraction
        # In production, use spaCy or similar
        
        # People mentions
        people_patterns = [
            r'\b(my\s+(mom|mother|dad|father|sister|brother|friend))\b',
            r'\b(parents?|family|siblings?)\b'
        ]
        
        for pattern in people_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'person',
                    'value': match[0] if isinstance(match, tuple) else match,
                    'role': 'family' if any(word in match.lower() for word in 
                                           ['mom', 'mother', 'dad', 'father', 'parent']) 
                            else 'friend'
                })
        
        # Issue mentions
        issue_keywords = {
            'school': ['school', 'exam', 'test', 'study', 'teacher'],
            'work': ['job', 'work', 'boss', 'colleague', 'unemployment'],
            'money': ['money', 'financial', 'bills', 'debt', 'poor'],
            'relationship': ['boyfriend', 'girlfriend', 'partner', 'breakup'],
            'health': ['sick', 'pain', 'hospital', 'doctor', 'medication']
        }
        
        for issue_type, keywords in issue_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                entities.append({
                    'type': 'issue',
                    'value': issue_type
                })
        
        return entities
    
    def identify_topics(self, text: str) -> List[str]:
        """Identify main topics in the text"""
        topics = []
        
        # Map keywords to topics
        topic_map = {
            'depression': ['sad', 'depressed', 'hopeless', 'empty', 'no energy'],
            'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'scared'],
            'stress': ['stressed', 'overwhelmed', 'pressure', 'burnout'],
            'relationships': ['friend', 'partner', 'family', 'argument', 'lonely'],
            'academic': ['school', 'exam', 'study', 'grades', 'teacher'],
            'financial': ['money', 'bills', 'debt', 'poor', 'unemployment']
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_map.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return list(set(topics))  # Remove duplicates
    
    def generate_recommendations(self, context: Dict, sentiment: Dict, 
                               topics: List[str], language: str) -> List[Dict]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Resource type based on risk level
        risk_level = context.get('risk_level', 'low')
        
        if risk_level in ['high', 'critical']:
            recommendations.append({
                'type': 'emergency',
                'title': 'Emergency Helpline',
                'description': 'Immediate professional support',
                'action': 'Call 0800-123-456',
                'urgency': 'high'
            })
        
        # Mood-based resources
        if sentiment['label'] == 'sad':
            recommendations.append({
                'type': 'exercise',
                'title': 'Mood Boosting Activity',
                'description': 'Simple activities to improve mood',
                'action': 'Try a 10-minute walk or listen to music',
                'urgency': 'low'
            })
        
        # Topic-based resources
        for topic in topics:
            if topic == 'academic':
                recommendations.append({
                    'type': 'article',
                    'title': 'Managing Academic Stress',
                    'description': 'Tips for handling school pressure',
                    'url': '/resources/academic-stress',
                    'urgency': 'medium'
                })
            elif topic == 'financial':
                recommendations.append({
                    'type': 'resource',
                    'title': 'Financial Counseling',
                    'description': 'Free financial advice services',
                    'action': 'Contact local youth support center',
                    'urgency': 'medium'
                })
        
        # Add breathing exercise for anxiety/stress
        if 'anxiety' in topics or 'stress' in topics:
            recommendations.append({
                'type': 'exercise',
                'title': '4-7-8 Breathing',
                'description': 'Calming breathing technique',
                'instructions': 'Breathe in for 4, hold for 7, exhale for 8',
                'duration': '2 minutes',
                'urgency': 'low'
            })
        
        # Localize titles and descriptions
        for rec in recommendations:
            rec['title'] = self.translate_text(rec['title'], language)
            if 'description' in rec:
                rec['description'] = self.translate_text(rec['description'], language)
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def generate_followup_questions(self, topics: List[str], language: str) -> List[str]:
        """Generate follow-up questions based on topics"""
        questions = []
        
        question_templates = {
            'depression': {
                'en': "How long have you been feeling this way?",
                'lg': "Waba ogudde emyeeki nga oli mutyo?",
                'sw': "Umekuwa hivyo kwa muda gani?"
            },
            'anxiety': {
                'en': "What situations make you feel most anxious?",
                'lg': "Ebintu ki ebikweraliikiriza nnyo?",
                'sw': "Hali gani zinakufanya ujisikie mwenye wasiwasi zaidi?"
            },
            'relationships': {
                'en': "How do these relationship issues affect your daily life?",
                'lg': "Ebizibu by'okwatagana biri kutandika otya mu bulamu bwo?",
                'sw': "Shida hizi za mahusiano zinakuaathiri vipi maisha yako ya kila siku?"
            },
            'academic': {
                'en': "What support do you wish you had with your studies?",
                'lg': "Kiki ekisigaddewo okukuyamba mu by'okusoma?",
                'sw': "Ungependa upate usaidizi gani katika masomo yako?"
            }
        }
        
        for topic in topics:
            if topic in question_templates:
                questions.append(question_templates[topic].get(
                    language, question_templates[topic]['en']
                ))
        
        # Add general follow-up if no specific questions
        if not questions:
            general_question = {
                'en': "What's one small thing that might help you feel better?",
                'lg': "Kintu kimu kitono kiki ekikuyinza okuyamba okwebaka obulungi?",
                'sw': "Ni jambo gani dogo linaweza kukusaidia kujisikia vizuri?"
            }
            questions.append(general_question.get(language, general_question['en']))
        
        return questions
    
    def culturally_adjust_response(self, response: str, language: str) -> str:
        """Adjust response for cultural appropriateness"""
        
        # Add cultural proverbs for Luganda
        if language == 'lg':
            proverbs = [
                "Okugamba nti 'nsonga teggwaawo' kitegeeza nti ebizibu bijja ne bigenda.",
                "Njogera: 'Akabi k'amazzi takaluma' kitegeeza nti ebizibu bya bulijjo tebisobola okukweraliikiriza."
            ]
            import random
            if random.random() < 0.3:  # 30% chance to add proverb
                response += f"\n\n{random.choice(proverbs)}"
        
        # Ensure respectful tone
        respectful_words = {
            'en': ['please', 'thank you', 'I understand', 'I hear you'],
            'lg': ['saba', 'webale', 'ntegeera', 'nkutte'],
            'sw': ['tafadhali', 'asante', 'ninaelewa', 'ninasikia']
        }
        
        # Check if response contains respectful language
        words = respectful_words.get(language, respectful_words['en'])
        if not any(word in response.lower() for word in words):
            # Add respectful opening
            openings = {
                'en': "Thank you for sharing that with me. ",
                'lg': "Webale okunnyonnyola ebyo. ",
                'sw': "Asante kwa kushiriki hilo. "
            }
            response = openings.get(language, openings['en']) + response
        
        return response
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Simple translation function"""
        # In production, use Google Translate API or similar
        # This is a simple mock translation
        
        translations = {
            'Emergency Helpline': {
                'lg': 'Ennamba ya Pulojekiti Eddakitibwa',
                'sw': 'Nambari ya Msaada wa Dharura'
            },
            'Mood Boosting Activity': {
                'lg': 'Ekintu Ekiyamba Okweyongeramu Ebyenjigiriza',
                'sw': 'Shughuli ya Kuboresha Hisia'
            }
        }
        
        if text in translations and target_language in translations[text]:
            return translations[text][target_language]
        
        return text
    
    def get_emergency_resources(self, location: str) -> List[Dict]:
        """Get emergency mental health resources for location"""
        
        uganda_resources = [
            {
                'name': 'National Mental Health Helpline',
                'contact': '0800-123-456',
                'hours': '24/7',
                'services': 'Crisis support, referrals'
            },
            {
                'name': 'Butabika National Referral Hospital',
                'contact': '0414-505-100',
                'hours': '24/7',
                'services': 'Emergency psychiatric care'
            },
            {
                'name': 'StrongMinds Uganda',
                'contact': '0772-456-789',
                'hours': '8am-6pm',
                'services': 'Depression therapy, support groups'
            },
            {
                'name': 'Mentality Uganda',
                'contact': '0701-234-567',
                'hours': '9am-5pm',
                'services': 'Youth counseling, online support'
            }
        ]
        
        return uganda_resources
    
    def format_chat_history(self, history: List[Dict]) -> str:
        """Format chat history for context"""
        formatted = []
        for msg in history:
            role = "User" if msg.get('role') == 'user' else "Assistant"
            content = msg.get('content', '')[:100]  # Truncate long messages
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted) if formatted else "No previous conversation."

# Singleton instance
tendo_ai = TendoAI()