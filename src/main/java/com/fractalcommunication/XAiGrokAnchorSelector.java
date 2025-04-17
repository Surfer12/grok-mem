package com.fractalcommunication;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

// Implementation of ML Anchor Selector using xAI Grok 3 Fast Beta
public class XAiGrokAnchorSelector implements IMLAnchorSelector {
  private final HttpClient httpClient;
  private final ObjectMapper objectMapper;
  private int successCount = 0;
  private int failureCount = 0;

  public XAiGrokAnchorSelector() {
    this.httpClient = HttpClient.newBuilder().connectTimeout(XAiConfig.getTimeout()).build();
    this.objectMapper = new ObjectMapper();
  }

  @Override
  public String selectAnchorWithML(
      IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors)
      throws FCFException {
    // Prepare prompt for xAI API
    String anchorList = availableAnchors.keySet().stream().collect(Collectors.joining(", "));
    String prompt =
        String.format(
            "You are a therapeutic conversational AI assistant. Based on the user's current input, conversation history, and profile, select the most appropriate therapeutic anchor from the following options: %s.\n\n"
                + "User Input: %s\n"
                + "Conversation History (recent): %s\n"
                + "User Interaction Style: %s\n"
                + "Preferred Anchors: %s\n\n"
                + "Respond with only the name of the selected anchor (e.g., 'Grounding') and a one-sentence rationale for why it was chosen.",
            anchorList,
            state.getUserInput(),
            state.getHistory().isEmpty()
                ? "No history yet."
                : String.join(
                    "; ",
                    state
                        .getHistory()
                        .subList(
                            Math.max(0, state.getHistory().size() - 3), state.getHistory().size())),
            state.getUserProfile().getInteractionStyle().toString(),
            state.getUserProfile().getPreferredAnchors().toString());

    // Prepare request payload (assuming similar structure to OpenAI)
    Map<String, Object> requestBody = new HashMap<>();
    requestBody.put("model", XAiConfig.getModel());
    requestBody.put(
        "messages",
        List.of(
            Map.of(
                "role",
                "system",
                "content",
                "You are a helpful assistant for selecting therapeutic conversational strategies."),
            Map.of("role", "user", "content", prompt)));
    requestBody.put("max_tokens", 50);
    requestBody.put("temperature", 0.3);

    try {
      // Serialize request body to JSON
      String jsonBody = objectMapper.writeValueAsString(requestBody);

      // Build HTTP request
      HttpRequest request =
          HttpRequest.newBuilder()
              .uri(URI.create(XAiConfig.getEndpoint()))
              .header("Authorization", "Bearer " + XAiConfig.getApiKey())
              .header("Content-Type", "application/json")
              .timeout(XAiConfig.getTimeout())
              .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
              .build();

      // Send request and get response
      HttpResponse<String> response =
          httpClient.send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() != 200) {
        throw new FCFException(
            "xAI API returned non-200 status: "
                + response.statusCode()
                + ", body: "
                + response.body(),
            null);
      }

      // Parse response (assuming similar structure to OpenAI)
      Map<String, Object> responseJson = objectMapper.readValue(response.body(), Map.class);
      List<Map<String, Object>> choices = (List<Map<String, Object>>) responseJson.get("choices");
      if (choices == null || choices.isEmpty()) {
        throw new FCFException("xAI API response missing choices", null);
      }
      Map<String, Object> message = (Map<String, Object>) choices.get(0).get("message");
      String responseText = (String) message.get("content");
      if (responseText == null || responseText.trim().isEmpty()) {
        throw new FCFException("xAI API response missing content", null);
      }

      // Extract anchor name from response
      String selectedAnchorName =
          responseText.split("\n")[0].trim().split(" ")[0].replace("'", "").replace("\"", "");
      if (!availableAnchors.containsKey(selectedAnchorName)) {
        throw new FCFException("xAI selected an invalid anchor: " + selectedAnchorName, null);
      }
      successCount++;
      System.out.println(
          "xAI selected anchor: " + selectedAnchorName + " with rationale: " + responseText);
      return selectedAnchorName;
    } catch (Exception e) {
      failureCount++;
      throw new FCFException("Failed to get anchor from xAI API: " + e.getMessage(), e);
    }
  }

  @Override
  public Map<String, Object> getSelectorMetrics() {
    return Map.of(
        "xAiSuccessCount", successCount,
        "xAiFailureCount", failureCount,
        "modelUsed", getModelName());
  }

  @Override
  public String getModelName() {
    return "xAI Grok 3 Fast Beta";
  }
}
