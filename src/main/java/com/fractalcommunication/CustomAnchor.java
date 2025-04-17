package com.fractalcommunication;

import java.util.Map;

// Concrete implementation of a custom therapeutic anchor
public class CustomAnchor implements ITherapeuticAnchor {
  private final String name;
  private final String description;
  private int usageCount = 0;

  public CustomAnchor(String name, String description) {
    this.name = name;
    this.description = description;
  }

  @Override
  public String getName() {
    return name;
  }

  @Override
  public String getDescription() {
    return description;
  }

  @Override
  public String apply(String reflection) {
    usageCount++;
    return reflection + " Applying custom anchor: " + description;
  }

  @Override
  public boolean validateSafety(String context) {
    // Micro-test for safety (e.g., avoid triggering phrases)
    return !context.toLowerCase().contains("unsafe");
  }

  @Override
  public Map<String, Object> getUsageMetrics() {
    return Map.of("usageCount", usageCount, "anchorName", name);
  }
}
