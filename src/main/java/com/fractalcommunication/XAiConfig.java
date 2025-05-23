package com.fractalcommunication;

import java.time.Duration;

// Configuration class for xAI API
class XAiConfig {
  private static final String MODEL = "grok-3-fast-beta"; // Hypothetical model name
  private static final String ENDPOINT =
      "https://api.x.ai/v1/chat/completions"; // Hypothetical endpoint
  private static final Duration TIMEOUT = Duration.ofSeconds(10);

  public static String getApiKey() {
    return EnvironmentLoader.getRequiredEnv(
        "XAI_API_KEY", 
        "xAI API key not found in environment variables or .env file.");
  }

  public static String getModel() {
    return MODEL;
  }

  public static String getEndpoint() {
    return ENDPOINT;
  }

  public static Duration getTimeout() {
    return TIMEOUT;
  }
}
