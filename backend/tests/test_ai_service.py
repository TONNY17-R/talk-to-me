"""Tests for AI service."""

import pytest
from backend.app.services.ai_service import AIService


class TestAIService:
    """Test AI service functionality."""
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis."""
        ai_service = AIService()
        sentiment = ai_service.analyze_sentiment("I am very happy")
        assert sentiment in ['negative', 'neutral', 'positive', 'very_negative', 'very_positive']
    
    def test_crisis_detection(self):
        """Test crisis detection."""
        ai_service = AIService()
        risk = ai_service.detect_crisis_indicators("I want to hurt myself")
        assert risk in ['low', 'medium', 'high', 'critical']
    
    def test_response_generation(self):
        """Test AI response generation."""
        ai_service = AIService()
        response = ai_service.generate_response("I am feeling sad")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_knowledge_base_response(self):
        """Test that knowledge base responses are returned for known queries."""
        ai_service = AIService()
        response = ai_service.generate_response("What is Talk to Me?")
        assert "Talk to Me" in response or "mental health" in response
