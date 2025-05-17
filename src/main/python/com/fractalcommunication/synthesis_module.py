#!/usr/bin/env python3
# Synthesis Module for Fractal Communication Framework

from com.fractalcommunication.anchor import IAnchor
import random

class SynthesisModule:
    def synthesize(self, reflection: str, anchor: IAnchor, user_history: list, anchor_name: str = '') -> str:
        # Multiple response templates
        templates = [
            "You mentioned: '{reflection}'. Let's explore {anchor_focus}. Try {anchor_action}—this can help {anchor_benefit}.",
            "Your input: '{reflection}'. Consider focusing on {anchor_focus}. {anchor_action} might be beneficial here.",
            "Reflecting on '{reflection}', I see a need for {anchor_focus}. How about {anchor_action}? This often helps {anchor_benefit}.",
            "Based on '{reflection}', let's look at {anchor_focus}. Perhaps {anchor_action} could improve {anchor_benefit}."
        ]
        
        # Select random template
        template = random.choice(templates)
        
        # Get anchor details
        anchor_focus = anchor.get_focus()
        anchor_action = anchor.get_action()
        anchor_benefit = anchor.get_benefit()
        
        # Default closing advice
        closing_advice = "Try to notice warmth in your heart as you express yourself—this can help maintain connection even in disagreement."
        
        # Vary closing advice based on anchor_name (explicitly passed)
        anchor_name = anchor_name.lower() if anchor_name else ''
        if anchor_name == 'grounding':
            closing_advice = "Focus on staying centered and calm—this can help you navigate challenges with clarity."
        elif anchor_name == 'openness':
            closing_advice = "Embrace this curiosity as a path to growth—this can open new ways of seeing and connecting."
        elif anchor_name == 'connection':
            closing_advice = "Hold space for empathy as you share—this can deepen understanding and trust."
        
        # Format response with closing advice
        response = template.format(
            reflection=reflection,
            anchor_focus=anchor_focus,
            anchor_action=anchor_action,
            anchor_benefit=anchor_benefit
        )
        return f"{response} {closing_advice}"
