package com.fractalcommunication;

import java.util.ArrayList;
import java.util.List;

// Concrete implementation of Conversation State
public class ConversationStateImpl implements IConversationState {
  private final String userInput;
  private final List<String> context;
  private final IUserProfile userProfile;
  private final List<String> history;

  public ConversationStateImpl(
      String userInput, List<String> context, IUserProfile userProfile, List<String> history) {
    this.userInput = userInput;
    this.context = new ArrayList<>(context);
    this.userProfile = userProfile;
    this.history = history;
  }

  @Override
  public String getUserInput() {
    return userInput;
  }

  @Override
  public List<String> getContext() {
    return new ArrayList<>(context);
  }

  @Override
  public IUserProfile getUserProfile() {
    return userProfile;
  }

  @Override
  public List<String> getHistory() {
    return new ArrayList<>(history);
  }

  @Override
  public void updateHistory(String entry) {
    history.add(entry);
  }
}
