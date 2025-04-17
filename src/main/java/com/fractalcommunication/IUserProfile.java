package com.fractalcommunication;

import java.util.List;
import java.util.Map;

// Interface for User Profile
public interface IUserProfile {
    String getUserId();
    Map<String, String> getInteractionStyle();
    List<String> getPreferredAnchors();
    void updateInteractionStyle(Map<String, String> newStyle);
}