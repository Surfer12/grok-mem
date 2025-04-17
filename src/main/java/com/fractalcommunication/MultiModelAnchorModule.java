package com.fractalcommunication;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Enhanced implementation of Anchor Module with support for multiple ML models
public class MultiModelAnchorModule implements IAnchorModule {
    private final Map<String, ITherapeuticAnchor> anchors = new HashMap<>();
    private int selectionCount = 0;
    private int successfulApplications = 0;
    private final IMetricsLogger metricsLogger;
    private final List<IMLAnchorSelector> mlSelectors;
    private final IMLAnchorSelector defaultSelector;

    public MultiModelAnchorModule(IMetricsLogger metricsLogger) {
        this.metricsLogger = metricsLogger;
        this.mlSelectors = new ArrayList<>();
        
        // Initialize xAI Grok 3 Fast Beta as default
        IMLAnchorSelector tempDefaultSelector = null;
        try {
            tempDefaultSelector = new XAiGrokAnchorSelector();
            this.mlSelectors.add(tempDefaultSelector);
        } catch (Exception e) {
            metricsLogger.logError("AnchorModule", "Failed to initialize xAI selector: " + e.getMessage(), e);
        }
        this.defaultSelector = tempDefaultSelector;

        // Add OpenAI as an alternative if xAI fails
        try {
            this.mlSelectors.add(new OpenAiAnchorSelector());
        } catch (Exception e) {
            metricsLogger.logError("AnchorModule", "Failed to initialize OpenAI selector: " + e.getMessage(), e);
        }

        // Register default anchors
        registerAnchor(new CustomAnchor("Grounding", "Focus on breath or body to create a safe container."));
        registerAnchor(new CustomAnchor("Openness", "Approach with curiosity, without judgment."));
        registerAnchor(new CustomAnchor("Connection", "Foster mutual understanding with warmth."));
        registerAnchor(new CustomAnchor("Transformation", "Identify a mindful action to shift patterns."));
        registerAnchor(new CustomAnchor("Integration", "Connect insights across domains."));
    }

    @Override
    public void registerAnchor(ITherapeuticAnchor anchor) {
        anchors.put(anchor.getName(), anchor);
        System.out.println("Registered anchor: " + anchor.getName());
    }

    @Override
    public ITherapeuticAnchor selectAnchor(IConversationState state) throws FCFException {
        selectionCount++;
        if (defaultSelector != null) {
            for (IMLAnchorSelector selector : mlSelectors) {
                try {
                    String anchorName = selector.selectAnchorWithML(state, anchors);
                    ITherapeuticAnchor selectedAnchor = anchors.get(anchorName);
                    if (selectedAnchor != null) {
                        metricsLogger.logMetric("AnchorModule", "mlSelectionSuccess", selector.getModelName());
                        return selectedAnchor;
                    }
                } catch (FCFException e) {
                    metricsLogger.logError("AnchorModule", "ML selector " + selector.getModelName() + " failed: " + e.getMessage(), e);
                }
            }
        }
        // Fallback to heuristic if all ML selectors fail
        fallbackCount++;
        metricsLogger.logMetric("AnchorModule", "fallbackTriggered", true);
        return fallbackAnchorSelection(state);
    }

    private int fallbackCount = 0;

    private ITherapeuticAnchor fallbackAnchorSelection(IConversationState state) throws FCFException {
        List<String> preferredAnchors = state.getUserProfile().getPreferredAnchors();
        if (!preferredAnchors.isEmpty()) {
            String preferred = preferredAnchors.get(0);
            ITherapeuticAnchor anchor = anchors.get(preferred);
            if (anchor != null) return anchor;
        }
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
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("selectionCount", selectionCount);
        metrics.put("successfulApplications", successfulApplications);
        metrics.put("fallbackCount", fallbackCount);
        mlSelectors.forEach(selector -> metrics.putAll(selector.getSelectorMetrics()));
        return metrics;
    }
}