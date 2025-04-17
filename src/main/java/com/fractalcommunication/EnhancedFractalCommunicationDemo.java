package com.fractalcommunication;

import java.util.List;

// Main class to demonstrate enhanced features
public class EnhancedFractalCommunicationDemo {
    public static void main(String[] args) {
        // Initialize components
        IMetricsLogger metricsLogger = new BasicMetricsLogger();
        IReflectionEngine reflectionEngine = new BasicReflectionEngine();
        IAnchorModule anchorModule = new BasicAnchorModule(metricsLogger);
        ISynthesisModule synthesisModule = new BasicSynthesisModule();
        IMemoryModule memoryModule = new MultiModalMemoryModule();
        IExerciseEngine exerciseEngine = new BasicExerciseEngine();

        IConversationOrchestrator orchestrator = new EnhancedConversationOrchestrator(
            reflectionEngine, anchorModule, synthesisModule, memoryModule, exerciseEngine, metricsLogger
        );

        // Simulate user interaction with error handling and branching
        String userId = "user123";
        String sessionId = "session456";
        String[] userInputs = {
            "I'm struggling to express disagreement without causing tension.",
            "Yeah, I do want to keep things peaceful, but I end up bottling things up."
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

        // Simulate an interruption
        try {
            orchestrator.handleInterruption(userId, sessionId, "User disengaged due to emotional spike");
            System.out.println("Interruption handled.");
        } catch (FCFException e) {
            System.err.println("Interruption error: " + e.getMessage());
        }

        // Simulate branching for a parallel exercise
        try {
            orchestrator.handleBranching(userId, sessionId, "parallel_exercise", "Exploring alternative anchors");
            System.out.println("Branching handled.");
        } catch (FCFException e) {
            System.err.println("Branching error: " + e.getMessage());
        }

        // Simulate generating an exercise
        System.out.println("\nGenerated Exercise for Challenge:");
        try {
            List<String> exerciseSteps = orchestrator.generateExercise(userInputs[0], userId, sessionId);
            exerciseSteps.forEach(step -> System.out.println("- " + step));
        } catch (FCFException e) {
            System.err.println("Exercise generation error: " + e.getMessage());
        }

        // Display metrics
        System.out.println("\nMetrics Summary:");
        metricsLogger.getAllMetrics().forEach((key, value) -> System.out.println(key + ": " + value));
    }
}