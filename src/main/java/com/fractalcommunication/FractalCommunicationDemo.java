package com.fractalcommunication;

import java.util.List;

// Main class to simulate basic interaction
public class FractalCommunicationDemo {
    public static void main(String[] args) {
        // Initialize components
        IReflectionEngine reflectionEngine = new BasicReflectionEngine();
        IAnchorModule anchorModule = new BasicAnchorModule(new BasicMetricsLogger());
        ISynthesisModule synthesisModule = new BasicSynthesisModule();
        IMemoryModule memoryModule = new MultiModalMemoryModule();
        IExerciseEngine exerciseEngine = new BasicExerciseEngine();
        IMetricsLogger metricsLogger = new BasicMetricsLogger();

        IConversationOrchestrator orchestrator = new EnhancedConversationOrchestrator(
            reflectionEngine, anchorModule, synthesisModule, memoryModule, exerciseEngine, metricsLogger
        );

        // Simulate user interaction
        String userId = "user123";
        String sessionId = "session456";
        String[] userInputs = {
            "I'm struggling to express disagreement without causing tension.",
            "Yeah, I do want to keep things peaceful, but I end up bottling things up.",
            "I’m curious now, but I’m still worried about upsetting others if I speak up.",
            "That warmth idea helps. I think I could try that, but I’m not sure how to start."
        };

        System.out.println("Conversation Simulation:");
        for (String input : userInputs) {
            System.out.println("\nUser Input: " + input);
            try {
                String response = orchestrator.runConversation(input, userId, sessionId);
                System.out.println("AI Response: " + response);
            } catch (FCFException e) {
                System.err.println("Error: " + e.getMessage());
            }
        }

        // Simulate generating an exercise
        System.out.println("\nGenerated Exercise for Challenge:");
        try {
            List<String> exerciseSteps = orchestrator.generateExercise(userInputs[0], userId, sessionId);
            exerciseSteps.forEach(step -> System.out.println("- " + step));
        } catch (FCFException e) {
            System.err.println("Exercise generation error: " + e.getMessage());
        }
    }
}