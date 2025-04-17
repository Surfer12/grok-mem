package com.fractalcommunication;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Concrete implementation of User Profile
public class UserProfileImpl implements IUserProfile {
    private final String userId;
    private final Map<String, String> interactionStyle;
    private final List<String> preferredAnchors;

    public UserProfileImpl(String userId, Map<String, String> interactionStyle, List<String> preferredAnchors) {
        this.userId = userId;
        this.interactionStyle = new HashMap<>(interactionStyle);
        this.preferredAnchors = new ArrayList<>(preferredAnchors);
    }

    @Override
    public String getUserId() { return userId; }

    @Override
    public Map<String, String> getInteractionStyle() { return new HashMap<>(interactionStyle); }

    @Override
    public List<String> getPreferredAnchors() { return new ArrayList<>(preferredAnchors); }

    @Override
    public void updateInteractionStyle(Map<String, String> newStyle) {
        interactionStyle.putAll(newStyle);
    }
}