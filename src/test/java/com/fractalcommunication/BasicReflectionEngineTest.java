package com.fractalcommunication;

import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class BasicReflectionEngineTest {

  private BasicReflectionEngine reflectionEngine;
  private IConversationState state;

  @BeforeEach
  public void setUp() {
    reflectionEngine = new BasicReflectionEngine();
    IUserProfile profile =
        new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding"));
    state =
        new ConversationStateImpl("Test input", List.of("Context 1"), profile, new ArrayList<>());
  }

  @Test
  public void testReflect() throws FCFException {
    String reflection = reflectionEngine.reflect(state);
    assertNotNull(reflection, "Reflection result should not be null.");
    assertTrue(reflection.contains("Reflecting on"), "Reflection should contain expected prefix.");
    assertTrue(reflection.contains("Test input"), "Reflection should include the user input.");
  }

  @Test
  public void testGetReflectionMetrics() {
    Map<String, Object> metrics = reflectionEngine.getReflectionMetrics();
    assertEquals(
        1,
        metrics.get("reflectionsPerformed"),
        "Reflections performed count should be 1 in metrics.");
  }
}
