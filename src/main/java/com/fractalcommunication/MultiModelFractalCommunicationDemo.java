package com.fractalcommunication;

// Main class to demonstrate multi-model anchor selection
public class MultiModelFractalCommunicationDemo {
  public static void main(String[] args) {
    // Initialize components
    IMetricsLogger metricsLogger = new BasicMetricsLogger();
    IReflectionEngine reflectionEngine = new BasicReflectionEngine();
    IAnchorModule anchorModule;
    try {
      anchorModule = new MultiModelAnchorModule(metricsLogger);
    } catch (Exception e) {
      System.err.println("Failed to initialize Multi-Model Anchor Module: " + e.getMessage());
      anchorModule = new BasicAnchorModule(metricsLogger); // Fallback to basic module
    }
    ISynthesisModule synthesisModule = new BasicSynthesisModule();
    IMemoryModule memoryModule = new MultiModalMemoryModule();
    IExerciseEngine exerciseEngine = new BasicExerciseEngine();

    IConversationOrchestrator orchestrator =
        new EnhancedConversationOrchestrator(
            reflectionEngine,
            anchorModule,
            synthesisModule,
            memoryModule,
            exerciseEngine,
            metricsLogger);

    // Simulate user interaction with multi-model anchor selection
    String userId = "user123";
    String sessionId = "session456";
    String[] userInputs = {
      "I'm struggling to express disagreement without causing tension.",
      "Yeah, I do want to keep things peaceful, but I end up bottling things up.",
      "I’m curious now, but I’m still worried about upsetting others if I speak up."
    };

    System.out.println(
        "Conversation Simulation with Multi-Model Anchor Selection (xAI Grok 3 Fast Beta Default):");
    for (String input : userInputs) {
      System.out.println("\nUser Input: " + input);
      try {
        String response = orchestrator.runConversation(input, userId, sessionId);
        System.out.println("AI Response: " + response);
      } catch (FCFException e) {
        System.err.println("Error: " + e.getMessage());
      }
    }

    // Display metrics
    System.out.println("\nMetrics Summary:");
    metricsLogger.getAllMetrics().forEach((key, value) -> System.out.println(key + ": " + value));
  }
}
