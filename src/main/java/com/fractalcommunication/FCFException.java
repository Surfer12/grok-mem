package com.fractalcommunication;

// Base exception for FCF-specific errors
public class FCFException extends Exception {
  public FCFException(String message, Throwable cause) {
    super(message, cause);
  }
}
