package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ConversationStateImplTest {

    private ConversationStateImpl state;
    private IUserProfile profile;
    private List<String> initialHistory;

    @BeforeEach
    public void setUp() {
        profile = new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding"));
        initialHistory = new ArrayList<>(List.of("History entry 1", "History entry 2"));
        state = new ConversationStateImpl("Test input", List.of("Context 1"), profile, initialHistory);
    }

    @Test
    public void testGetUserInput() {
        assertEquals("Test input", state.getUserInput(), "User input should match the initialized value.");
    }

    @Test
    public void testGetContext() {
        List<String> context = state.getContext();
        assertEquals(1, context.size(), "Context list should have 1 element.");
        assertEquals("Context 1", context.get(0), "Context content should match the initialized value.");
        assertNotSame(context, state.getContext(), "Context should return a copy to prevent modification of internal state.");
    }

    @Test
    public void testGetUserProfile() {
        assertEquals(profile, state.getUserProfile(), "User profile should match the initialized value.");
    }

    @Test
    public void testGetHistory() {
        List<String> history = state.getHistory();
        assertEquals(2, history.size(), "History list should have 2 elements.");
        assertEquals("History entry 1", history.get(0), "First history entry should match.");
        assertEquals("History entry 2", history.get(1), "Second history entry should match.");
        assertNotSame(history, state.getHistory(), "History should return a copy to prevent modification of internal state.");
    }

    @Test
    public void testUpdateHistory() {
        String newEntry = "New history entry";
        state.updateHistory(newEntry);
        List<String> history = state.getHistory();
        assertEquals(3, history.size(), "History list should have 3 elements after update.");
        assertEquals(newEntry, history.get(2), "New history entry should be added at the end.");
        assertNotSame(initialHistory, history, "GetHistory should return a copy, not the internal list.");
    }
}