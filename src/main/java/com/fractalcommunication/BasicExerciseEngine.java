package com.fractalcommunication;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

// Placeholder implementation of Exercise Engine
public class BasicExerciseEngine implements IExerciseEngine {
  @Override
  public List<String> generateSteps(ITherapeuticAnchor[] frameworkSteps, String challenge)
      throws FCFException {
    List<String> steps = new ArrayList<>();
    steps.add("Challenge: " + challenge);
    for (int i = 0; i < frameworkSteps.length; i++) {
      steps.add("Step " + (i + 1) + ": " + frameworkSteps[i].getName());
    }
    return steps;
  }

  @Override
  public Map<String, Object> getExerciseMetrics() {
    return Map.of("exercisesGenerated", 1);
  }
}
