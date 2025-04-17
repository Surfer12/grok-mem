package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class BasicMetricsLoggerTest {

    private BasicMetricsLogger metricsLogger;

    @BeforeEach
    public void setUp() {
        metricsLogger = new BasicMetricsLogger();
    }

    @Test
    public void testLogMetric() {
        metricsLogger.logMetric("TestModule", "testMetric", 42);
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("TestModule_testMetric_count"), "Metric count should be 1 after logging a single metric.");
    }

    @Test
    public void testLogMetric_MultipleValues() {
        metricsLogger.logMetric("TestModule", "multiMetric", 10);
        metricsLogger.logMetric("TestModule", "multiMetric", 20);
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(2, metrics.get("TestModule_multiMetric_count"), "Metric count should be 2 after logging two values for the same metric.");
    }

    @Test
    public void testLogError() {
        metricsLogger.logError("ErrorModule", "Test error message", null);
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("ErrorModule_error_count"), "Error count should be 1 after logging a single error.");
    }

    @Test
    public void testLogError_WithCause() {
        Exception cause = new Exception("Cause of error");
        metricsLogger.logError("ErrorModule", "Test error with cause", cause);
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("ErrorModule_error_count"), "Error count should be 1 after logging an error with a cause.");
    }

    @Test
    public void testGetAllMetrics_Empty() {
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertTrue(metrics.isEmpty(), "Metrics should be empty when no metrics or errors are logged.");
    }

    @Test
    public void testGetAllMetrics_Mixed() {
        metricsLogger.logMetric("MixedModule", "testMetric", 100);
        metricsLogger.logError("MixedModule", "Test error", null);
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("MixedModule_testMetric_count"), "Metric count should be 1 for logged metric.");
        assertEquals(1, metrics.get("MixedModule_error_count"), "Error count should be 1 for logged error.");
    }
}