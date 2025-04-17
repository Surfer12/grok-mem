package com.fractalcommunication;

import java.util.List;

// Interface for Orchestrator with error handling and branching
public interface IConversationOrchestrator {
  String runConversation(String userInput, String userId, String sessionId) throws FCFException;

  List<String> generateExercise(String challenge, String userId, String sessionId)
      throws FCFException;

  void handleInterruption(String userId, String sessionId, String reason) throws FCFException;

  void handleBranching(String userId, String sessionId, String branchType, String data)
      throws FCFException;

  String fallbackRoutine(String userInput, String userId, String sessionId) throws FCFException;
}
