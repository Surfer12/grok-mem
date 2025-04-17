package com.fractalcommunication;

import java.util.Map;

// Interface for Reflection Engine (z²)
public interface IReflectionEngine {
    String reflect(IConversationState state) throws FCFException;
    Map<String, Object> getReflectionMetrics(); // Metrics for analysis
}