package com.fractalcommunication;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Concrete implementation of Metrics Logger
public class BasicMetricsLogger implements IMetricsLogger {
  private final Map<String, List<Object>> metrics = new HashMap<>();
  private final Map<String, List<String>> errors = new HashMap<>();

  @Override
  public void logMetric(String moduleName, String metricName, Object value) {
    metrics.computeIfAbsent(moduleName + "_" + metricName, _ -> new ArrayList<Object>()).add(value);
    System.out.println("Logged metric: " + moduleName + " - " + metricName + " = " + value);
  }

  @Override
  public void logError(String moduleName, String errorMessage, Throwable cause) {
    errors
        .computeIfAbsent(moduleName, key -> new ArrayList<String>())
        .add(errorMessage + (cause != null ? " Cause: " + cause.getMessage() : ""));
    System.err.println("Logged error in " + moduleName + ": " + errorMessage);
  }

  @Override
  public Map<String, Object> getAllMetrics() {
    Map<String, Object> allMetrics = new HashMap<>();
    metrics.forEach((key, values) -> allMetrics.put(key + "_count", values.size()));
    errors.forEach((key, errs) -> allMetrics.put(key + "_error_count", errs.size()));
    return allMetrics;
  }
}
