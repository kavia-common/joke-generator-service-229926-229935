#!/bin/bash
cd /home/kavia/workspace/code-generation/joke-generator-service-229926-229935/joke_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

