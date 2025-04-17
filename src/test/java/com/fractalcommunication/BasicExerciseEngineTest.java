package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

public class BasicExerciseEngineTest {

    private BasicExerciseEngine exerciseEngine;

    @BeforeEach
    public void setUp() {
        exerciseEngine = new BasicExerciseEngine();
    }

    @Test
    public void testGenerateSteps() throws FCFException {
        String challenge = "Test challenge";
        ITherapeuticAnchor[] steps = {
            new CustomAnchor("Grounding", "Focus on breath."),
            new CustomAnchor("Openness", "Approach with curiosity.")
        };
        List<String> result = exerciseEngine.generateSteps(steps, challenge);
        assertNotNull(result, "Generated steps should not be null.");
        assertEquals(3, result.size(), "Result should have 3 elements (challenge + 2 steps).");
        assertEquals("Challenge: " + challenge, result.get(0), "First element should be the challenge description.");
        assertEquals("Step 1: Grounding", result.get(1), "First step should match the first anchor name.");
        assertEquals("Step 2: Openness", result.get(2), "Second step should match the second anchor name.");
    }

    @Test
    public void testGetExerciseMetrics() {
        Map<String, Object> metrics = exerciseEngine.getExerciseMetrics();
        assertEquals(1, metrics.get("exercisesGenerated"), "Exercises generated count should be 1 in metrics.");
    }
}