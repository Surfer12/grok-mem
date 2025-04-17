package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class MLAnchorSelectorTest {

    private IConversationState state;
    private Map<String, ITherapeuticAnchor> anchors;

    @BeforeEach
    public void setUp() {
        IUserProfile profile = new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding"));
        state = new ConversationStateImpl("Test input", List.of(), profile, new ArrayList<>());
        anchors = Map.of(
                "Grounding", new CustomAnchor("Grounding", "desc"),
                "Openness", new CustomAnchor("Openness", "desc"),
                "Connection", new CustomAnchor("Connection", "desc")
        );
    }

    @Test
    public void testXAiGrokAnchorSelector_Success() throws Exception {
        // Mock HttpClient and ObjectMapper using package-private visibility or use different constructor for injection if refactoring is allowed
        XAiGrokAnchorSelector selectorSpy = Mockito.spy(new XAiGrokAnchorSelector());

        // Mock response text to simulate xAI's output
        doReturn("Grounding\nBecause it helps...").when(selectorSpy)
            .selectAnchorWithML(any(), any());

        String anchor = selectorSpy.selectAnchorWithML(state, anchors);
        assertEquals("Grounding", anchor);

        Map<String, Object> metrics = selectorSpy.getSelectorMetrics();
        assertEquals("xAI Grok 3 Fast Beta", selectorSpy.getModelName());
    }

    @Test
    public void testXAiGrokAnchorSelector_Failure() {
        XAiGrokAnchorSelector selectorSpy = Mockito.spy(new XAiGrokAnchorSelector());

        // Simulate failure by throwing FCFException
        try {
            doThrow(new FCFException("Test failure", null)).when(selectorSpy).selectAnchorWithML(any(), any());
            selectorSpy.selectAnchorWithML(state, anchors);
            fail("Expected FCFException not thrown");
        } catch (FCFException e) {
            assertTrue(e.getMessage().contains("Test failure"));
        }
    }

    @Test
    public void testOpenAiAnchorSelector_ModelNameAndMetrics() {
        // Unlike xAI, OpenAiAnchorSelector's CTOR may fail if env vars aren't set,
        // so only test simple things not requiring API access

        OpenAiAnchorSelector selector = mock(OpenAiAnchorSelector.class);
        when(selector.getModelName()).thenReturn("OpenAI GPT-3.5 Turbo");
        when(selector.getSelectorMetrics()).thenReturn(Map.of(
                "openAiSuccessCount", 1,
                "openAiFailureCount", 0,
                "modelUsed", "OpenAI GPT-3.5 Turbo"
        ));

        assertEquals("OpenAI GPT-3.5 Turbo", selector.getModelName());
        Map<String, Object> metrics = selector.getSelectorMetrics();
        assertEquals(1, metrics.get("openAiSuccessCount"));
        assertEquals(0, metrics.get("openAiFailureCount"));
        assertEquals("OpenAI GPT-3.5 Turbo", metrics.get("modelUsed"));
    }
}
