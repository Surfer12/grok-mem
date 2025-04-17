package com.fractalcommunication;

import com.theokanning.openai.completion.chat.ChatCompletionRequest;
import com.theokanning.openai.completion.chat.ChatMessage;
import com.theokanning.openai.completion.chat.ChatMessageRole;
import com.theokanning.openai.service.OpenAiService;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

// Implementation of ML Anchor Selector using OpenAI as an alternative
public class OpenAiAnchorSelector implements IMLAnchorSelector {
  private final OpenAiService openAiService;
  private int successCount = 0;
  private int failureCount = 0;

  public OpenAiAnchorSelector() {
    try {
      this.openAiService = OpenAiConfig.getService();
    } catch (IllegalStateException e) {
      throw new IllegalStateException("Failed to initialize OpenAI service: " + e.getMessage(), e);
    }
  }

  @Override
  public String selectAnchorWithML(
      IConversationState state, Map<String, ITherapeuticAnchor> availableAnchors)
      throws FCFException {
    // Similar to previous OpenAI implementation
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

    List<ChatMessage> messages = new ArrayList<>();
    messages.add(
        new ChatMessage(
            ChatMessageRole.SYSTEM.value(),
            "You are a helpful assistant for selecting therapeutic conversational strategies."));
    messages.add(new ChatMessage(ChatMessageRole.USER.value(), prompt));

    ChatCompletionRequest request =
        ChatCompletionRequest.builder()
            .model(OpenAiConfig.getModel())
            .messages(messages)
            .maxTokens(50)
            .temperature(0.3)
            .build();

    try {
      var response = openAiService.createChatCompletion(request);
      String responseText = response.getChoices().get(0).getMessage().getContent().trim();
      String selectedAnchorName =
          responseText.split("\n")[0].trim().split(" ")[0].replace("'", "").replace("\"", "");
      if (!availableAnchors.containsKey(selectedAnchorName)) {
        throw new FCFException("OpenAI selected an invalid anchor: " + selectedAnchorName, null);
      }
      successCount++;
      System.out.println(
          "OpenAI selected anchor: " + selectedAnchorName + " with rationale: " + responseText);
      return selectedAnchorName;
    } catch (Exception e) {
      failureCount++;
      throw new FCFException("Failed to get anchor from OpenAI API: " + e.getMessage(), e);
    }
  }

  @Override
  public Map<String, Object> getSelectorMetrics() {
    return Map.of(
        "openAiSuccessCount", successCount,
        "openAiFailureCount", failureCount,
        "modelUsed", getModelName());
  }

  @Override
  public String getModelName() {
    return "OpenAI GPT-3.5 Turbo";
  }
}
