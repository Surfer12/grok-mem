package com.fractalcommunication;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Concrete implementation of Conversation Orchestrator with error handling and branching
public class EnhancedConversationOrchestrator implements IConversationOrchestrator {
  private final IReflectionEngine reflectionEngine;
  private final IAnchorModule anchorModule;
  private final ISynthesisModule synthesisModule;
  private final IMemoryModule memoryModule;
  private final IExerciseEngine exerciseEngine;
  private final IMetricsLogger metricsLogger;
  private final Map<String, List<String>> activeBranches =
      new HashMap<>(); // userId_sessionId -> branchData

  public EnhancedConversationOrchestrator(
      IReflectionEngine reflectionEngine,
      IAnchorModule anchorModule,
      ISynthesisModule synthesisModule,
      IMemoryModule memoryModule,
      IExerciseEngine exerciseEngine,
      IMetricsLogger metricsLogger) {
    this.reflectionEngine = reflectionEngine;
    this.anchorModule = anchorModule;
    this.synthesisModule = synthesisModule;
    this.memoryModule = memoryModule;
    this.exerciseEngine = exerciseEngine;
    this.metricsLogger = metricsLogger;
  }

  @Override
  public String runConversation(String userInput, String userId, String sessionId)
      throws FCFException {
    try {
      IUserProfile profile = memoryModule.loadUserProfile(userId);
      IConversationState state =
          new ConversationStateImpl(userInput, List.of(), profile, new ArrayList<>());

      String reflection = reflectionEngine.reflect(state);
      metricsLogger.logMetric("ReflectionEngine", "reflectionLength", reflection.length());

      ITherapeuticAnchor anchor = anchorModule.selectAnchor(state);
      String anchoredResponse = anchorModule.applyAnchor(reflection, anchor);
      metricsLogger.logMetric("AnchorModule", "selectedAnchor", anchor.getName());

      String synthesizedOutput = synthesisModule.synthesize(reflection, anchoredResponse);
      metricsLogger.logMetric("SynthesisModule", "outputLength", synthesizedOutput.length());

      memoryModule.saveShortTermInteraction(userId, synthesizedOutput, sessionId);
      state.updateHistory(userInput + " -> " + synthesizedOutput);
      return synthesizedOutput;
    } catch (FCFException e) {
      metricsLogger.logError("Orchestrator", "Conversation error: " + e.getMessage(), e);
      return fallbackRoutine(userInput, userId, sessionId);
    }
  }

  @Override
  public List<String> generateExercise(String challenge, String userId, String sessionId)
      throws FCFException {
    try {
      ITherapeuticAnchor[] steps = {
        new CustomAnchor("Grounding", "Focus on breath or body."),
        new CustomAnchor("Openness", "Approach with curiosity."),
        new CustomAnchor("Connection", "Foster mutual understanding.")
      };
      List<String> exerciseSteps = exerciseEngine.generateSteps(steps, challenge);
      memoryModule.saveSessionMemory(userId, sessionId, String.join("\n", exerciseSteps));
      metricsLogger.logMetric("ExerciseEngine", "exerciseStepsGenerated", exerciseSteps.size());
      return exerciseSteps;
    } catch (FCFException e) {
      metricsLogger.logError("Orchestrator", "Exercise generation error: " + e.getMessage(), e);
      throw e;
    }
  }

  @Override
  public void handleInterruption(String userId, String sessionId, String reason)
      throws FCFException {
    String key = userId + "_" + sessionId;
    activeBranches.computeIfAbsent(key, k -> new ArrayList<>()).add("Interruption: " + reason);
    metricsLogger.logMetric("Orchestrator", "interruptionHandled", reason);
    memoryModule.saveShortTermInteraction(userId, "Interruption logged: " + reason, sessionId);
  }

  @Override
  public void handleBranching(String userId, String sessionId, String branchType, String data)
      throws FCFException {
    String key = userId + "_" + sessionId;
    activeBranches
        .computeIfAbsent(key, k -> new ArrayList<>())
        .add("Branch: " + branchType + " - " + data);
    metricsLogger.logMetric("Orchestrator", "branchCreated", branchType);
    memoryModule.saveSessionMemory(userId, sessionId, "Branch added: " + branchType);
  }

  @Override
  public String fallbackRoutine(String userInput, String userId, String sessionId)
      throws FCFException {
    String fallbackMessage =
        "I'm having trouble processing that. Could you clarify what you mean by '"
            + userInput
            + "'?";
    metricsLogger.logMetric("Orchestrator", "fallbackTriggered", "true");
    memoryModule.saveShortTermInteraction(userId, "Fallback: " + fallbackMessage, sessionId);
    return fallbackMessage;
  }
}
