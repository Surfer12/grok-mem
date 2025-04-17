package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@ExtendWith(MockitoExtension.class)
public class MLAnchorSelectorTest {

    @Mock
    private IConversationState state;

    private Map<String, ITherapeuticAnchor> availableAnchors;

    @BeforeEach
    public void setUp() {
        availableAnchors = new HashMap<>();
        availableAnchors.put("Grounding", new CustomAnchor("Grounding", "Focus on breath."));
        availableAnchors.put("Openness", new CustomAnchor("Openness", "Approach with curiosity."));
        availableAnchors.put("Connection", new CustomAnchor("Connection", "Foster warmth."));
    }

    @Test
    public void testXAiGrokAnchorSelector_ModelNameAndMetrics() {
        // Since Mockito can't mock the class directly due to inline mock issues, we'll test a wrapped behavior or use a stub
        XAiGrokAnchorSelector selector = new XAiGrokAnchorSelectorStub();
        assertEquals("xAI Grok 3 Fast Beta", selector.getModelName(), "Model name should match xAI Grok 3 Fast Beta.");

        Map<String, Object> metrics = selector.getSelectorMetrics();
        assertTrue(metrics.containsKey("xAiSuccessCount"), "Metrics should contain xAI success count.");
        assertTrue(metrics.containsKey("xAiFailureCount"), "Metrics should contain xAI failure count.");
        assertTrue(metrics.containsKey("modelUsed"), "Metrics should contain model used.");
    }

    @Test
    public void testOpenAiAnchorSelector_ModelNameAndMetrics() {
        // Similar stub approach for OpenAI due to mocking limitations
        OpenAiAnchorSelector selector = new OpenAiAnchorSelectorStub();
        assertEquals("OpenAI GPT-3.5 Turbo", selector.getModelName(), "Model name should match OpenAI GPT-3.5 Turbo.");

        Map<String, Object> metrics = selector.getSelectorMetrics();
        assertTrue(metrics.containsKey("openAiSuccessCount"), "Metrics should contain OpenAI success count.");
        assertTrue(metrics.containsKey("openAiFailureCount"), "Metrics should contain OpenAI failure count.");
        assertTrue(metrics.containsKey("modelUsed"), "Metrics should contain model used.");
    }

    // Stub class to avoid direct API calls or complex mocking in tests
    private static class XAiGrokAnchorSelectorStub extends XAiGrokAnchorSelector {
        @Override
        public String selectAnchorWithML(IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors) throws FCFException {
            return "Grounding"; // Stubbed response
        }
    }

    private static class OpenAiAnchorSelectorStub extends OpenAiAnchorSelector {
        @Override
        public String selectAnchorWithML(IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors) throws FCFException {
            return "Openness"; // Stubbed response
        }
    }
}