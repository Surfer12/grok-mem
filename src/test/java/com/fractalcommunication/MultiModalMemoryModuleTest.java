package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import java.util.Optional;

public class MultiModalMemoryModuleTest {

    private MultiModalMemoryModule memoryModule;

    @BeforeEach
    public void setUp() {
        memoryModule = new MultiModalMemoryModule();
    }

    @Test
    public void testLoadUserProfile_NewUser() throws FCFException {
        IUserProfile profile = memoryModule.loadUserProfile("newUser");
        assertNotNull(profile, "Profile should not be null for a new user.");
        assertEquals("newUser", profile.getUserId(), "User ID should match the requested ID.");
        assertEquals("fractal", profile.getInteractionStyle().get("style"), "Default interaction style should be set.");
        assertEquals(1, profile.getPreferredAnchors().size(), "Default preferred anchors should be set.");
        assertEquals("connection", profile.getPreferredAnchors().get(0), "Default preferred anchor should be 'connection'.");
    }

    @Test
    public void testLoadUserProfile_ExistingUser() throws FCFException {
        IUserProfile profile1 = memoryModule.loadUserProfile("existingUser");
        IUserProfile profile2 = memoryModule.loadUserProfile("existingUser");
        assertSame(profile1, profile2, "Loading the same user ID should return the same profile instance.");
    }

    @Test
    public void testSaveShortTermInteraction() throws FCFException {
        String userId = "user123";
        String sessionId = "session456";
        String data = "Short term interaction data";
        memoryModule.saveShortTermInteraction(userId, data, sessionId);
        Optional<String> retrieved = memoryModule.retrieveShortTermInteraction(userId, sessionId);
        assertTrue(retrieved.isPresent(), "Short term interaction should be retrievable.");
        assertEquals(data, retrieved.get(), "Retrieved data should match saved data.");
    }

    @Test
    public void testSaveLongTermInteractionStyle() throws FCFException {
        String userId = "user123";
        Map<String, String> newStyle = Map.of("style", "updated", "mode", "therapeutic");
        memoryModule.saveLongTermInteractionStyle(userId, newStyle);
        IUserProfile profile = memoryModule.loadUserProfile(userId);
        assertEquals("updated", profile.getInteractionStyle().get("style"), "Interaction style should be updated.");
        assertEquals("therapeutic", profile.getInteractionStyle().get("mode"), "New interaction style entry should be added.");
    }

    @Test
    public void testSaveSessionMemory() throws FCFException {
        String userId = "user123";
        String sessionId = "session456";
        String exerciseData = "Exercise data for session";
        memoryModule.saveSessionMemory(userId, sessionId, exerciseData);
        // Indirectly test by checking metrics since there's no direct retrieval method
        Map<String, Object> metrics = memoryModule.getMemoryMetrics();
        assertEquals(1, metrics.get("activeSessions"), "Active sessions count should reflect saved session memory.");
    }

    @Test
    public void testRetrieveShortTermInteraction_NonExistent() throws FCFException {
        String userId = "nonexistent";
        String sessionId = "session999";
        Optional<String> retrieved = memoryModule.retrieveShortTermInteraction(userId, sessionId);
        assertFalse(retrieved.isPresent(), "Non-existent interaction should return empty Optional.");
    }

    @Test
    public void testGetMemoryMetrics() throws FCFException {
        String userId = "user123";
        String sessionId = "session456";
        memoryModule.saveShortTermInteraction(userId, "Data", sessionId);
        memoryModule.saveLongTermInteractionStyle(userId, Map.of("style", "updated"));
        memoryModule.saveSessionMemory(userId, sessionId, "Exercise data");

        Map<String, Object> metrics = memoryModule.getMemoryMetrics();
        assertEquals(1, metrics.get("shortTermSaves"), "Short term saves count should be incremented.");
        assertEquals(1, metrics.get("longTermSaves"), "Long term saves count should be incremented.");
        assertEquals(1, metrics.get("activeSessions"), "Active sessions count should be incremented.");
    }
}