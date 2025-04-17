package com.fractalcommunication;

import java.util.Map;

// Placeholder implementation of Reflection Engine
public class BasicReflectionEngine implements IReflectionEngine {
  @Override
  public String reflect(IConversationState state) throws FCFException {
    return "Reflecting on: " + state.getUserInput();
  }

  @Override
  public Map<String, Object> getReflectionMetrics() {
    return Map.of("reflectionsPerformed", 1);
  }
}
