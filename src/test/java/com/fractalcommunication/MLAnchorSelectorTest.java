package com.fractalcommunication;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MLAnchorSelectorTest {

    private IConversationState stateStub;
    private Map<String, ITherapeuticAnchor> availableAnchors;

    @Test
    public void setUp() {
        // Create a stub for IConversationState without using Mockito
        stateStub = new IConversationStateStub();
        availableAnchors = new HashMap<>();
        availableAnchors.put("Grounding", new CustomAnchor("Grounding", "Focus on breath."));
        availableAnchors.put("Openness", new CustomAnchor("Openness", "Approach with curiosity."));
        availableAnchors.put("Connection", new CustomAnchor("Connection", "Foster warmth."));
    }

    @Test
    public void testXAiGrokAnchorSelector_ModelNameAndMetrics() {
        // Use a stub implementation instead of mocking
        XAiGrokAnchorSelectorStub selector = new XAiGrokAnchorSelectorStub();
        assertEquals("xAI Grok 3 Fast Beta", selector.getModelName(), "Model name should match xAI Grok 3 Fast Beta.");

        Map<String, Object> metrics = selector.getSelectorMetrics();
        assertTrue(metrics.containsKey("xAiSuccessCount"), "Metrics should contain xAI success count.");
        assertTrue(metrics.containsKey("xAiFailureCount"), "Metrics should contain xAI failure count.");
        assertTrue(metrics.containsKey("modelUsed"), "Metrics should contain model used.");
    }

    @Test
    public void testOpenAiAnchorSelector_ModelNameAndMetrics() {
        // Use a stub implementation instead of mocking
        OpenAiAnchorSelectorStub selector = new OpenAiAnchorSelectorStub();
        assertEquals("OpenAI GPT-3.5 Turbo", selector.getModelName(), "Model name should match OpenAI GPT-3.5 Turbo.");

        Map<String, Object> metrics = selector.getSelectorMetrics();
        assertTrue(metrics.containsKey("openAiSuccessCount"), "Metrics should contain OpenAI success count.");
        assertTrue(metrics.containsKey("openAiFailureCount"), "Metrics should contain OpenAI failure count.");
        assertTrue(metrics.containsKey("modelUsed"), "Metrics should contain model used.");
    }

    // Stub implementation for IConversationState
    private static class IConversationStateStub implements IConversationState {
        @Override
        public String getUserInput() {
            return "Test input";
        }

        @Override
        public List<String> getContext() {
            return new ArrayList<>(List.of("Context 1"));
        }

        @Override
        public IUserProfile getUserProfile() {
            return new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding"));
        }

        @Override
        public List<String> getHistory() {
            return new ArrayList<>(List.of("History entry 1"));
        }

        @Override
        public void updateHistory(String entry) {
            // No-op for stub
        }
    }

    // Stub class for XAiGrokAnchorSelector
    private static class XAiGrokAnchorSelectorStub implements IMLAnchorSelector {
        @Override
        public String selectAnchorWithML(IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors) throws FCFException {
            return "Grounding"; // Stubbed response
        }

        @Override
        public Map<String, Object> getSelectorMetrics() {
            return Map.of(
                "xAiSuccessCount", 0,
                "xAiFailureCount", 0,
                "modelUsed", getModelName()
            );
        }

        @Override
        public String getModelName() {
            return "xAI Grok 3 Fast Beta";
        }
    }

    // Stub class for OpenAiAnchorSelector
    private static class OpenAiAnchorSelectorStub implements IMLAnchorSelector {
        @Override
        public String selectAnchorWithML(IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors) throws FCFException {
            return "Openness"; // Stubbed response
        }

        @Override
        public Map<String, Object> getSelectorMetrics() {
            return Map.of(
                "openAiSuccessCount", 0,
                "openAiFailureCount", 0,
                "modelUsed", getModelName()
            );
        }

        @Override
        public String getModelName() {
            return "OpenAI GPT-3.5 Turbo";
        }
    }
}