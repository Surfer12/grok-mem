#!/usr/bin/env python3
# Persona Module for Fractal Communication Framework

from typing import Dict, List, Optional
import random

class Persona:
    """
    Represents a simulated user with specific communication preferences and patterns.
    Useful for testing the FCF system with diverse user types.
    """
    
    def __init__(
        self,
        name: str,
        personality_traits: Dict[str, float],
        communication_style: Dict[str, float],
        primary_concerns: List[str],
        vocabulary_level: str = "average"
    ):
        """
        Initialize a new persona.
        
        Args:
            name: Identifier for this persona
            personality_traits: Dict of traits (e.g., "openness", "anxiety") with values 0.0-1.0
            communication_style: Dict of style preferences (e.g., "direct", "emotional") with values 0.0-1.0
            primary_concerns: List of topics/concerns this persona typically focuses on
            vocabulary_level: One of "basic", "average", "advanced" to simulate different expression capabilities
        """
        self.name = name
        self.personality_traits = personality_traits
        self.communication_style = communication_style
        self.primary_concerns = primary_concerns
        self.vocabulary_level = vocabulary_level
        
        # Internal state for conversation simulation
        self._satisfaction_level = 0.5  # Start neutral (0.0-1.0)
        self._previous_responses = []
        
    def generate_prompt(self, context: Optional[str] = None, scenario: Optional[str] = None) -> str:
        """
        Generate a prompt/query based on this persona's characteristics.
        
        Args:
            context: Optional contextual information to shape the prompt
            scenario: Optional specific scenario to address
            
        Returns:
            A generated user prompt that simulates this persona's communication style
        """
        # Select from persona's primary concerns if no scenario provided
        if not scenario:
            topic = random.choice(self.primary_concerns)
        else:
            topic = scenario
            
        # Build prompt based on communication style and traits
        directness = self.communication_style.get("direct", 0.5)
        emotionality = self.communication_style.get("emotional", 0.5)
        anxiety = self.personality_traits.get("anxiety", 0.3)
        
        # Phrases reflecting different communication styles
        direct_phrases = [
            f"I need help with {topic}.",
            f"Tell me how to deal with {topic}.",
            f"What's your advice about {topic}?",
            f"I want to know about {topic}."
        ]
        
        indirect_phrases = [
            f"I've been thinking about {topic} lately...",
            f"Do you have any thoughts on {topic}?",
            f"I'm not sure if this makes sense, but {topic} has been on my mind.",
            f"I wonder if you could help me understand {topic} better?"
        ]
        
        emotional_phrases = [
            f"I'm really frustrated about {topic}.",
            f"I'm excited to learn more about {topic}!",
            f"I'm worried about {topic} and don't know what to do.",
            f"I feel overwhelmed when I think about {topic}."
        ]
        
        anxious_addendums = [
            " Sorry if that's a silly question.",
            " I hope that makes sense.",
            " I'm not sure if I'm explaining this correctly.",
            " I know this might be difficult to answer."
        ]
        
        # Select phrase based on directness and emotionality
        phrases = []
        if random.random() < directness:
            phrases.extend(direct_phrases)
        else:
            phrases.extend(indirect_phrases)
            
        if random.random() < emotionality:
            phrases.extend(emotional_phrases)
            
        prompt = random.choice(phrases)
        
        # Add anxious qualifier if the persona has anxiety trait
        if random.random() < anxiety:
            prompt += random.choice(anxious_addendums)
            
        return prompt
        
    def evaluate_response(self, response: str) -> float:
        """
        Evaluate a response based on persona preferences.
        Returns satisfaction score 0.0-1.0
        """
        satisfaction = 0.5  # Start neutral
        
        # Check for resonance with communication style
        if self.communication_style.get("direct", 0.5) > 0.7:
            # Direct communicators prefer concise responses
            if len(response) < 300:
                satisfaction += 0.2
            else:
                satisfaction -= 0.1
                
        if self.communication_style.get("emotional", 0.5) > 0.7:
            # Emotional communicators prefer emotional language
            emotional_words = ["feel", "emotion", "heart", "connect", "understand"]
            if any(word in response.lower() for word in emotional_words):
                satisfaction += 0.2
            else:
                satisfaction -= 0.1
                
        # Check for persona-specific traits
        if self.personality_traits.get("anxiety", 0.0) > 0.7:
            # Anxious personas respond well to reassurance
            reassurance_words = ["normal", "common", "many people", "it's okay", "natural"]
            if any(word in response.lower() for word in reassurance_words):
                satisfaction += 0.2
                
        if self.personality_traits.get("openness", 0.0) > 0.7:
            # Open personas like novel perspectives
            if "perspective" in response.lower() or "consider" in response.lower():
                satisfaction += 0.1
                
        # Ensure satisfaction stays in 0.0-1.0 range
        satisfaction = max(0.0, min(1.0, satisfaction))
        
        # Update internal state
        self._satisfaction_level = satisfaction
        self._previous_responses.append(response)
        
        return satisfaction
        
    def get_satisfaction_level(self) -> float:
        """Get current satisfaction level with conversation."""
        return self._satisfaction_level
        
    @classmethod
    def create_standard_personas(cls) -> Dict[str, 'Persona']:
        """
        Create a set of standard test personas covering different user types.
        
        Returns:
            Dictionary of persona name -> Persona object
        """
        personas = {}
        
        # Analytical, direct communicator
        personas["analytical"] = cls(
            name="analytical",
            personality_traits={
                "openness": 0.6,
                "conscientiousness": 0.8,
                "extraversion": 0.4,
                "agreeableness": 0.5,
                "neuroticism": 0.3,
                "anxiety": 0.2
            },
            communication_style={
                "direct": 0.9,
                "emotional": 0.2,
                "verbose": 0.7,
                "formal": 0.8
            },
            primary_concerns=[
                "improving efficiency",
                "solving complex problems",
                "understanding data patterns",
                "optimizing processes"
            ],
            vocabulary_level="advanced"
        )
        
        # Emotional, relationship-focused communicator
        personas["emotional"] = cls(
            name="emotional",
            personality_traits={
                "openness": 0.7,
                "conscientiousness": 0.5,
                "extraversion": 0.8,
                "agreeableness": 0.9,
                "neuroticism": 0.6,
                "anxiety": 0.4
            },
            communication_style={
                "direct": 0.4,
                "emotional": 0.9,
                "verbose": 0.8,
                "formal": 0.3
            },
            primary_concerns=[
                "building better relationships",
                "managing difficult conversations",
                "expressing feelings appropriately",
                "connecting with others"
            ],
            vocabulary_level="average"
        )
        
        # Anxious, cautious communicator
        personas["anxious"] = cls(
            name="anxious",
            personality_traits={
                "openness": 0.4,
                "conscientiousness": 0.7,
                "extraversion": 0.3,
                "agreeableness": 0.6,
                "neuroticism": 0.9,
                "anxiety": 0.9
            },
            communication_style={
                "direct": 0.2,
                "emotional": 0.7,
                "verbose": 0.5,
                "formal": 0.6
            },
            primary_concerns=[
                "managing anxiety in conversations",
                "avoiding conflict",
                "making the right impression",
                "communicating without misunderstandings"
            ],
            vocabulary_level="average"
        )
        
        # Practical, problem-solving communicator
        personas["practical"] = cls(
            name="practical",
            personality_traits={
                "openness": 0.4,
                "conscientiousness": 0.8,
                "extraversion": 0.5,
                "agreeableness": 0.6,
                "neuroticism": 0.3,
                "anxiety": 0.2
            },
            communication_style={
                "direct": 0.8,
                "emotional": 0.3,
                "verbose": 0.3,
                "formal": 0.4
            },
            primary_concerns=[
                "solving immediate problems",
                "getting practical advice",
                "finding efficient solutions",
                "implementing actionable steps"
            ],
            vocabulary_level="average"
        )
        
        return personas