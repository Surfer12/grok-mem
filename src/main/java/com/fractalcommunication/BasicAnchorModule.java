package com.fractalcommunication;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

// Concrete implementation of Anchor Module with plug-in support
public class BasicAnchorModule implements IAnchorModule {
    private final Map<String, ITherapeuticAnchor> anchors = new HashMap<>();
    private int selectionCount = 0;
    private int successfulApplications = 0;
    private final IMetricsLogger metricsLogger;

    public BasicAnchorModule(IMetricsLogger metricsLogger) {
        this.metricsLogger = metricsLogger;
        // Default anchors
        registerAnchor(new CustomAnchor("Grounding", "Focus on breath or body to create a safe container."));
        registerAnchor(new CustomAnchor("Openness", "Approach with curiosity, without judgment."));
        registerAnchor(new CustomAnchor("Connection", "Foster mutual understanding with warmth."));
    }

    @Override
    public void registerAnchor(ITherapeuticAnchor anchor) {
        anchors.put(anchor.getName(), anchor);
        System.out.println("Registered anchor: " + anchor.getName());
    }

    @Override
    public ITherapeuticAnchor selectAnchor(IConversationState state) throws FCFException {
        selectionCount++;
        // Simple selection logic based on history size
        int index = state.getHistory().size() % anchors.size();
        String anchorName = new ArrayList<>(anchors.keySet()).get(index);
        ITherapeuticAnchor selected = anchors.get(anchorName);
        if (selected == null) {
            throw new FCFException("No anchor found for name: " + anchorName, null);
        }
        return selected;
    }

    @Override
    public String applyAnchor(String reflection, ITherapeuticAnchor anchor) throws FCFException {
        if (!anchor.validateSafety(reflection)) {
            throw new FCFException("Anchor " + anchor.getName() + " failed safety validation", null);
        }
        successfulApplications++;
        metricsLogger.logMetric("AnchorModule", "anchorApplicationSuccess", anchor.getName());
        return anchor.apply(reflection);
    }

    @Override
    public Map<String, Object> getAnchorSelectionMetrics() {
        return Map.of("selectionCount", selectionCount, "successfulApplications", successfulApplications);
    }
}