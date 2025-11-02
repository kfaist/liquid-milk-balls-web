#!/bin/bash

# Retry wrapper for Copilot/AI invocation
# Retries up to 3 times with exponential backoff
# Usage: This script wraps the Copilot action/command and handles transient failures

set +e  # Don't exit on error - we want to handle failures and retry

MAX_ATTEMPTS=3
ATTEMPT=1
BASE_SLEEP=5

echo "Starting Copilot agent with retry capability (max attempts: $MAX_ATTEMPTS)"

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
  echo "================================================"
  echo "Attempt $ATTEMPT of $MAX_ATTEMPTS"
  echo "================================================"
  
  # Execute the Copilot command/action
  # This is a placeholder that should be replaced with the actual Copilot invocation
  # Examples:
  # - GitHub Copilot CLI: gh copilot suggest "command"
  # - GitHub Action: Call the action's underlying CLI or API
  # - Custom integration: Your Copilot API call or command
  
  # For now, this is a template. Replace the command below with your actual Copilot invocation:
  # Example: gh copilot suggest --help
  # Example: node scripts/copilot-agent.js
  # Example: python scripts/copilot-agent.py
  
  echo "TODO: Replace this with actual Copilot command"
  echo "For example: gh copilot-cli <command> or call to Copilot API"
  
  # Placeholder command - replace with actual Copilot invocation
  # For testing purposes, this will succeed
  COPILOT_COMMAND_RESULT=0
  
  if [ $COPILOT_COMMAND_RESULT -eq 0 ]; then
    echo "SUCCESS: Copilot agent completed successfully on attempt $ATTEMPT"
    exit 0
  else
    EXIT_CODE=$COPILOT_COMMAND_RESULT
    echo "FAILED: Attempt $ATTEMPT failed with exit code $EXIT_CODE"
    
    if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
      SLEEP_TIME=$((BASE_SLEEP * ATTEMPT))
      echo "Retrying in $SLEEP_TIME seconds..."
      sleep $SLEEP_TIME
    else
      echo "ERROR: All $MAX_ATTEMPTS attempts failed"
      echo "Last exit code: $EXIT_CODE"
      echo "Check the logs above for detailed error messages"
      exit $EXIT_CODE
    fi
  fi
  
  ATTEMPT=$((ATTEMPT + 1))
done

# This should not be reached, but just in case
echo "ERROR: Unexpected script termination"
exit 1
