package com.fractalcommunication;

import java.util.Map;

// Interface for Therapeutic Anchor (plug-in support)
public interface ITherapeuticAnchor {
  String getName();

  String getDescription();

  String apply(String reflection); // Behavior definition for anchor

  boolean validateSafety(String context); // Micro-test for safety

  Map<String, Object> getUsageMetrics();
}
