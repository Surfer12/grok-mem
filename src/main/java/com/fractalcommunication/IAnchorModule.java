package com.fractalcommunication;

import java.util.Map;

// Interface for Anchor Module (c)
public interface IAnchorModule {
    ITherapeuticAnchor selectAnchor(IConversationState state) throws FCFException;
    String applyAnchor(String reflection, ITherapeuticAnchor anchor) throws FCFException;
    void registerAnchor(ITherapeuticAnchor anchor); // For plug-in support
    Map<String, Object> getAnchorSelectionMetrics();
}