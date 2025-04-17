package com.fractalcommunication;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class BasicSynthesisModuleTest {

  private BasicSynthesisModule synthesisModule;

  @BeforeEach
  public void setUp() {
    synthesisModule = new BasicSynthesisModule();
  }

  @Test
  public void testSynthesize() throws FCFException {
    String reflection = "Reflecting on user input";
    String anchoredResponse = "Applying anchor to reflection";
    String result = synthesisModule.synthesize(reflection, anchoredResponse);
    assertNotNull(result, "Synthesis result should not be null.");
    assertTrue(result.contains("Synthesized"), "Result should contain synthesis prefix.");
    assertTrue(result.contains(reflection), "Result should contain the original reflection.");
    assertTrue(result.contains(anchoredResponse), "Result should contain the anchored response.");
  }

  @Test
  public void testGetSynthesisMetrics() {
    Map<String, Object> metrics = synthesisModule.getSynthesisMetrics();
    assertEquals(
        1, metrics.get("synthesesPerformed"), "Syntheses performed count should be 1 in metrics.");
  }
}
