package com.fractalcommunication;

import com.theokanning.openai.service.OpenAiService;
import java.time.Duration;

// Utility class to manage OpenAI API configuration
class OpenAiConfig {
  private static final String MODEL = "gpt-3.5-turbo"; // Can be upgraded to gpt-4 if available
  private static final Duration TIMEOUT = Duration.ofSeconds(10);

  public static OpenAiService getService() {
    String apiKey = EnvironmentLoader.getRequiredEnv(
        "OPENAI_API_KEY", 
        "OpenAI API key not found in environment variables or .env file.");
    return new OpenAiService(apiKey, TIMEOUT);
  }

  public static String getModel() {
    return MODEL;
  }
}
