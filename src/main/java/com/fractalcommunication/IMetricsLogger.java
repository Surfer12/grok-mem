package com.fractalcommunication;

import java.util.Map;

// Interface for Metrics Logger
public interface IMetricsLogger {
  void logMetric(String moduleName, String metricName, Object value);

  void logError(String moduleName, String errorMessage, Throwable cause);

  Map<String, Object> getAllMetrics();
}
