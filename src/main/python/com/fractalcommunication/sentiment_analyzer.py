#!/usr/bin/env python3
# Sentiment Analysis Module for Fractal Communication Framework

from transformers import pipeline
import logging

class SentimentAnalyzer:
    def __init__(self):
        try:
            # Initialize the sentiment analysis pipeline
            self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            self.is_initialized = True
            logging.info("Sentiment analysis pipeline initialized successfully.")
        except Exception as e:
            self.is_initialized = False
            logging.error(f"Failed to initialize sentiment analysis pipeline: {str(e)}")
            # Fallback to basic keyword-based sentiment analysis
            self._initialize_keyword_fallback()
    
    def _initialize_keyword_fallback(self):
        """Initialize a simple keyword-based sentiment analyzer as fallback"""
        self.positive_keywords = [
            "happy", "glad", "good", "great", "excellent", "wonderful", "love", "enjoy", 
            "appreciate", "excited", "satisfied", "thankful", "pleased"
        ]
        self.negative_keywords = [
            "sad", "angry", "upset", "frustrated", "disappointed", "hate", "dislike", 
            "terrible", "awful", "annoying", "difficult", "hard", "confused", "worry", 
            "concerned", "anxious", "unhappy", "bad", "worst", "trouble", "problem", "hurt"
        ]
        logging.info("Fallback keyword sentiment analyzer initialized.")
    
    def analyze(self, text):
        """Analyze the sentiment of the input text
        
        Returns:
            dict: Contains sentiment label (POSITIVE/NEGATIVE/NEUTRAL) and score
        """
        try:
            if self.is_initialized:
                # Use the transformer model for analysis
                result = self.sentiment_pipeline(text)[0]
                # Standardize the output format
                return {
                    "label": result["label"],
                    "score": result["score"],
                    "method": "transformer"
                }
            else:
                # Use the keyword-based fallback
                return self._keyword_sentiment(text)
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {str(e)}")
            # In case of any errors, fall back to neutral sentiment
            return {"label": "NEUTRAL", "score": 0.5, "method": "fallback"}
    
    def _keyword_sentiment(self, text):
        """Simple keyword-based sentiment analysis"""
        text = text.lower()
        positive_count = sum(1 for word in self.positive_keywords if word in text)
        negative_count = sum(1 for word in self.negative_keywords if word in text)
        
        if positive_count > negative_count:
            return {"label": "POSITIVE", "score": min(0.5 + (positive_count * 0.1), 0.99), "method": "keyword"}
        elif negative_count > positive_count:
            return {"label": "NEGATIVE", "score": min(0.5 + (negative_count * 0.1), 0.99), "method": "keyword"}
        else:
            return {"label": "NEUTRAL", "score": 0.5, "method": "keyword"}

# For testing
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    test_texts = [
        "I'm really happy with the results!",
        "This is very frustrating and difficult.",
        "The sky is blue and the weather is nice."
    ]
    
    for text in test_texts:
        sentiment = analyzer.analyze(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']:.2f}, Method: {sentiment['method']}\n")
