package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

public class UserProfileImplTest {

    private UserProfileImpl userProfile;

    @BeforeEach
    public void setUp() {
        userProfile = new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding", "Connection"));
    }

    @Test
    public void testGetUserId() {
        assertEquals("user123", userProfile.getUserId(), "User ID should match the initialized value.");
    }

    @Test
    public void testGetInteractionStyle() {
        Map<String, String> style = userProfile.getInteractionStyle();
        assertEquals("fractal", style.get("style"), "Interaction style should match the initialized value.");
        assertNotSame(style, userProfile.getInteractionStyle(), "Interaction style should return a copy to prevent modification of internal state.");
    }

    @Test
    public void testGetPreferredAnchors() {
        List<String> anchors = userProfile.getPreferredAnchors();
        assertEquals(2, anchors.size(), "Preferred anchors list should have 2 elements.");
        assertEquals("Grounding", anchors.get(0), "First preferred anchor should be Grounding.");
        assertEquals("Connection", anchors.get(1), "Second preferred anchor should be Connection.");
        assertNotSame(anchors, userProfile.getPreferredAnchors(), "Preferred anchors should return a copy to prevent modification of internal state.");
    }

    @Test
    public void testUpdateInteractionStyle() {
        Map<String, String> newStyle = Map.of("style", "updated", "mode", "therapeutic");
        userProfile.updateInteractionStyle(newStyle);
        Map<String, String> updatedStyle = userProfile.getInteractionStyle();
        assertEquals("updated", updatedStyle.get("style"), "Interaction style should be updated.");
        assertEquals("therapeutic", updatedStyle.get("mode"), "New interaction style entry should be added.");
    }
}