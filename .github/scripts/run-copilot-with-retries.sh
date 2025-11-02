#!/bin/bash

# Retry wrapper for Copilot/AI invocation
# Retries up to 3 times with exponential backoff
# Usage: This script wraps the Copilot action/command and handles transient failures

set -e

MAX_ATTEMPTS=3
ATTEMPT=1
BASE_SLEEP=5

echo "Starting Copilot agent with retry capability (max attempts: $MAX_ATTEMPTS)"

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
  echo "================================================"
  echo "Attempt $ATTEMPT of $MAX_ATTEMPTS"
  echo "================================================"
  
  # Execute the Copilot command/action
  # Replace this with the actual Copilot CLI command or action invocation
  # For example:
  # - If using GitHub Copilot CLI: gh copilot suggest "command"
  # - If using a specific action: call the action's CLI wrapper
  # - If using API: curl to Copilot API endpoint
  
  if copilot_command; then
    echo "SUCCESS: Copilot agent completed successfully on attempt $ATTEMPT"
    exit 0
  else
    EXIT_CODE=$?
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
