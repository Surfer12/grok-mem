package com.fractalcommunication;

import com.theokanning.openai.service.OpenAiService;
import java.time.Duration;

// Utility class to manage OpenAI API configuration
class OpenAiConfig {
  private static final String API_KEY =
      System.getenv("OPENAI_API_KEY"); // Securely load from environment
  private static final String MODEL = "gpt-3.5-turbo"; // Can be upgraded to gpt-4 if available
  private static final Duration TIMEOUT = Duration.ofSeconds(10);

  public static OpenAiService getService() {
    if (API_KEY == null || API_KEY.isEmpty()) {
      throw new IllegalStateException("OpenAI API key not found in environment variables.");
    }
    return new OpenAiService(API_KEY, TIMEOUT);
  }

  public static String getModel() {
    return MODEL;
  }
}
