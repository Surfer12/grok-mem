package com.fractalcommunication;

import io.github.cdimascio.dotenv.Dotenv;

/**
 * Utility class for loading environment variables from .env files and system environment.
 * Handles API keys and other configuration values with proper fallback mechanisms.
 */
public class EnvironmentLoader {
    private static Dotenv dotenv;
    
    static {
        try {
            // Load from .env file if available
            dotenv = Dotenv.configure()
                    .ignoreIfMissing()
                    .load();
        } catch (Exception e) {
            System.err.println("Warning: Failed to load .env file: " + e.getMessage());
            // Continue without dotenv if loading fails
        }
    }
    
    /**
     * Gets an environment variable from .env file or system environment.
     * Prioritizes .env file values over system environment variables.
     *
     * @param key The environment variable key
     * @return The value from .env or system environment, or null if not found
     */
    public static String getEnv(String key) {
        String value = null;
        
        // Try to get from .env first
        if (dotenv != null) {
            try {
                value = dotenv.get(key);
            } catch (Exception e) {
                // Ignore dotenv errors and fallback to system env
            }
        }
        
        // Fallback to system environment if not found in .env
        if (value == null || value.isEmpty()) {
            value = System.getenv(key);
        }
        
        return value;
    }
    
    /**
     * Gets a required environment variable. Throws exception if not found.
     *
     * @param key The environment variable key
     * @param errorMessage Custom error message if variable is not found
     * @return The environment variable value
     * @throws IllegalStateException if the environment variable is not found
     */
    public static String getRequiredEnv(String key, String errorMessage) {
        String value = getEnv(key);
        if (value == null || value.isEmpty()) {
            throw new IllegalStateException(errorMessage);
        }
        return value;
    }
}
