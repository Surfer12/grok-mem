package com.fractalcommunication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

public class EnhancedConversationOrchestratorTest {

    private EnhancedConversationOrchestrator orchestrator;
    private IMetricsLogger metricsLogger;
    private IReflectionEngine reflectionEngine;
    private IAnchorModule anchorModule;
    private ISynthesisModule synthesisModule;
    private IMemoryModule memoryModule;
    private IExerciseEngine exerciseEngine;

    @BeforeEach
    public void setUp() {
        metricsLogger = new BasicMetricsLogger();
        reflectionEngine = new BasicReflectionEngine();
        anchorModule = new BasicAnchorModule(metricsLogger);
        synthesisModule = new BasicSynthesisModule();
        memoryModule = new MultiModalMemoryModule();
        exerciseEngine = new BasicExerciseEngine();
        orchestrator = new EnhancedConversationOrchestrator(
            reflectionEngine, anchorModule, synthesisModule, memoryModule, exerciseEngine, metricsLogger
        );
    }

    @Test
    public void testRunConversation_SuccessfulExecution() throws FCFException {
        String userInput = "I'm feeling stuck.";
        String userId = "user123";
        String sessionId = "session456";
        String response = orchestrator.runConversation(userInput, userId, sessionId);
        assertNotNull(response, "Response should not be null.");
        assertTrue(response.contains("Reflecting on"), "Response should contain reflection output.");
        assertTrue(response.contains("Applying custom anchor"), "Response should contain anchor application output.");

        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("ReflectionEngine_reflectionLength_count"), "Reflection metrics should be logged.");
        assertEquals(1, metrics.get("AnchorModule_selectedAnchor_count"), "Anchor selection metrics should be logged.");
        assertEquals(1, metrics.get("SynthesisModule_outputLength_count"), "Synthesis metrics should be logged.");
    }

    @Test
    public void testGenerateExercise_SuccessfulExecution() throws FCFException {
        String challenge = "Test challenge";
        String userId = "user123";
        String sessionId = "session456";
        List<String> steps = orchestrator.generateExercise(challenge, userId, sessionId);
        assertNotNull(steps, "Exercise steps should not be null.");
        assertFalse(steps.isEmpty(), "Exercise steps should not be empty.");
        assertEquals("Challenge: " + challenge, steps.get(0), "First step should be the challenge description.");

        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("ExerciseEngine_exerciseStepsGenerated_count"), "Exercise generation metrics should be logged.");
    }

    @Test
    public void testHandleInterruption() throws FCFException {
        String userId = "user123";
        String sessionId = "session456";
        String reason = "Emotional spike";
        orchestrator.handleInterruption(userId, sessionId, reason);
        
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("Orchestrator_interruptionHandled_count"), "Interruption handling metrics should be logged.");
    }

    @Test
    public void testHandleBranching() throws FCFException {
        String userId = "user123";
        String sessionId = "session456";
        String branchType = "parallel_exercise";
        String data = "Exploring alternatives";
        orchestrator.handleBranching(userId, sessionId, branchType, data);
        
        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("Orchestrator_branchCreated_count"), "Branch creation metrics should be logged.");
    }

    @Test
    public void testFallbackRoutine() throws FCFException {
        String userInput = "Confusing input";
        String userId = "user123";
        String sessionId = "session456";
        String fallbackResponse = orchestrator.fallbackRoutine(userInput, userId, sessionId);
        assertTrue(fallbackResponse.contains(userInput), "Fallback response should mention the user input.");
        assertTrue(fallbackResponse.contains("clarify"), "Fallback response should ask for clarification.");

        Map<String, Object> metrics = metricsLogger.getAllMetrics();
        assertEquals(1, metrics.get("Orchestrator_fallbackTriggered_count"), "Fallback metrics should be logged.");
    }
}