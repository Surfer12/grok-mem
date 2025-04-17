package com.fractalcommunication;

import java.util.Map;

// Interface for ML-based anchor selection to support multiple models
public interface IMLAnchorSelector {
    String selectAnchorWithML(IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors) throws FCFException;
    Map<String, Object> getSelectorMetrics();
    String getModelName();
}