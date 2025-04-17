package com.fractalcommunication;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

// Concrete implementation of Memory Module with multi-modal storage
public class MultiModalMemoryModule implements IMemoryModule {
    private final Map<String, IUserProfile> profiles = new HashMap<>();
    private final Map<String, String> shortTermMemory = new HashMap<>(); // userId_sessionId -> data
    private final Map<String, String> sessionMemory = new HashMap<>(); // userId_sessionId -> exerciseData
    private int shortTermSaves = 0;
    private int longTermSaves = 0;

    @Override
    public IUserProfile loadUserProfile(String userId) throws FCFException {
        return profiles.computeIfAbsent(userId, k -> new UserProfileImpl(userId, Map.of("style", "fractal"), java.util.List.of("connection")));
    }

    @Override
    public void saveShortTermInteraction(String userId, String data, String sessionId) throws FCFException {
        shortTermMemory.put(userId + "_" + sessionId, data);
        shortTermSaves++;
    }

    @Override
    public void saveLongTermInteractionStyle(String userId, Map<String, String> styleData) throws FCFException {
        IUserProfile profile = loadUserProfile(userId);
        profile.updateInteractionStyle(styleData);
        longTermSaves++;
    }

    @Override
    public void saveSessionMemory(String userId, String sessionId, String exerciseData) throws FCFException {
        sessionMemory.put(userId + "_" + sessionId, exerciseData);
    }

    @Override
    public Optional<String> retrieveShortTermInteraction(String userId, String sessionId) throws FCFException {
        return Optional.ofNullable(shortTermMemory.get(userId + "_" + sessionId));
    }

    @Override
    public Map<String, Object> getMemoryMetrics() {
        return Map.of("shortTermSaves", shortTermSaves, "longTermSaves", longTermSaves, "activeSessions", sessionMemory.size());
    }
}