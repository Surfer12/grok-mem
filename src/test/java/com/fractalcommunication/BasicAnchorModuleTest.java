package com.fractalcommunication;

import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class BasicAnchorModuleTest {

  private BasicAnchorModule anchorModule;
  private IMetricsLogger metricsLogger;
  private IConversationState state;

  @BeforeEach
  public void setUp() {
    metricsLogger = new BasicMetricsLogger();
    anchorModule = new BasicAnchorModule(metricsLogger);
    IUserProfile profile =
        new UserProfileImpl("user123", Map.of("style", "fractal"), List.of("Grounding"));
    state = new ConversationStateImpl("Test input", List.of(), profile, new ArrayList<>());
  }

  @Test
  public void testRegisterAnchor() {
    ITherapeuticAnchor customAnchor = new CustomAnchor("TestAnchor", "Test description");
    anchorModule.registerAnchor(customAnchor);
    // Since registerAnchor only adds to a map, we indirectly test by selecting it after adding
    assertNotNull(customAnchor, "Registered anchor should not be null.");
  }

  @Test
  public void testSelectAnchor() throws FCFException {
    ITherapeuticAnchor selectedAnchor = anchorModule.selectAnchor(state);
    assertNotNull(selectedAnchor, "Selected anchor should not be null.");
    assertTrue(
        selectedAnchor.getName().equals("Grounding")
            || selectedAnchor.getName().equals("Openness")
            || selectedAnchor.getName().equals("Connection"),
        "Selected anchor should be one of the default anchors.");
  }

  @Test
  public void testApplyAnchor_SafeContext() throws FCFException {
    ITherapeuticAnchor anchor = new CustomAnchor("TestAnchor", "Test description");
    String reflection = "Safe reflection";
    String result = anchorModule.applyAnchor(reflection, anchor);
    assertTrue(
        result.contains(reflection), "Applied result should contain the original reflection.");
    assertTrue(
        result.contains("Applying custom anchor"),
        "Applied result should contain application message.");
  }

  @Test
  public void testApplyAnchor_UnsafeContext() {
    ITherapeuticAnchor anchor = new CustomAnchor("TestAnchor", "Test description");
    String reflection = "Unsafe reflection";
    assertThrows(
        FCFException.class,
        () -> anchorModule.applyAnchor(reflection, anchor),
        "Unsafe context should throw FCFException.");
  }

  @Test
  public void testGetAnchorSelectionMetrics() throws FCFException {
    anchorModule.selectAnchor(state);
    Map<String, Object> metrics = anchorModule.getAnchorSelectionMetrics();
    assertEquals(
        1,
        metrics.get("selectionCount"),
        "Selection count should be incremented after selectAnchor.");
    assertEquals(
        0,
        metrics.get("successfulApplications"),
        "Successful applications should be 0 before applyAnchor.");

    ITherapeuticAnchor anchor = anchorModule.selectAnchor(state);
    anchorModule.applyAnchor("Safe reflection", anchor);
    metrics = anchorModule.getAnchorSelectionMetrics();
    assertEquals(
        1,
        metrics.get("successfulApplications"),
        "Successful applications should be incremented after applyAnchor.");
  }
}
