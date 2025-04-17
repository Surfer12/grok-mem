package com.fractalcommunication;

import java.util.Map;
import java.util.Optional;

// Interface for Memory Module (multi-modal)
public interface IMemoryModule {
    IUserProfile loadUserProfile(String userId) throws FCFException;
    void saveShortTermInteraction(String userId, String data, String sessionId) throws FCFException;
    void saveLongTermInteractionStyle(String userId, Map<String, String> styleData) throws FCFException;
    void saveSessionMemory(String userId, String sessionId, String exerciseData) throws FCFException;
    Optional<String> retrieveShortTermInteraction(String userId, String sessionId) throws FCFException;
    Map<String, Object> getMemoryMetrics();
}