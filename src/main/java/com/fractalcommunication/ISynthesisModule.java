package com.fractalcommunication;

import java.util.Map;

// Interface for Synthesis Module (new z)
public interface ISynthesisModule {
    String synthesize(String reflection, String anchoredResponse) throws FCFException;
    Map<String, Object> getSynthesisMetrics();
}