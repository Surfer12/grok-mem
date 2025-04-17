package com.fractalcommunication;

import java.util.List;
import java.util.Map;

// Interface for Exercise Engine
public interface IExerciseEngine {
  List<String> generateSteps(ITherapeuticAnchor[] frameworkSteps, String challenge)
      throws FCFException;

  Map<String, Object> getExerciseMetrics();
}
