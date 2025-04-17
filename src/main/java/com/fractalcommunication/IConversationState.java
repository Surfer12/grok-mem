package com.fractalcommunication;

import java.util.List;

// Interface for Conversation State to abstract state management
public interface IConversationState {
    String getUserInput();
    List<String> getContext();
    IUserProfile getUserProfile();
    List<String> getHistory();
    void updateHistory(String entry);
}