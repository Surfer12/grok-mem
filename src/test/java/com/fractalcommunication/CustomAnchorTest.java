package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;

public class CustomAnchorTest {

    private CustomAnchor anchor;

    @BeforeEach
    public void setUp() {
        anchor = new CustomAnchor("Grounding", "Focus on breath or body to create a safe container.");
    }

    @Test
    public void testGetName() {
        assertEquals("Grounding", anchor.getName(), "Anchor name should match the initialized value.");
    }

    @Test
    public void testGetDescription() {
        assertEquals("Focus on breath or body to create a safe container.", anchor.getDescription(), "Anchor description should match the initialized value.");
    }

    @Test
    public void testApply() {
        String reflection = "Reflecting on user input";
        String result = anchor.apply(reflection);
        assertTrue(result.contains(reflection), "Applied result should contain the original reflection.");
        assertTrue(result.contains("Applying custom anchor"), "Applied result should contain application message.");
    }

    @Test
    public void testValidateSafety_SafeContext() {
        String safeContext = "This is a safe reflection.";
        assertTrue(anchor.validateSafety(safeContext), "Safe context should pass validation.");
    }

    @Test
    public void testValidateSafety_UnsafeContext() {
        String unsafeContext = "This is an unsafe reflection.";
        assertFalse(anchor.validateSafety(unsafeContext), "Unsafe context should fail validation.");
    }

    @Test
    public void testGetUsageMetrics() {
        // Apply the anchor to increment usage count
        anchor.apply("Test reflection");
        Map<String, Object> metrics = anchor.getUsageMetrics();
        assertEquals(1, metrics.get("usageCount"), "Usage count should be incremented after apply.");
        assertEquals("Grounding", metrics.get("anchorName"), "Anchor name in metrics should match.");
    }
}