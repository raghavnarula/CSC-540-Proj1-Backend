#!/bin/bash

# This section generates curl commands and saves them in a temporary file
temp_file=$(mktemp)

# Define the roles
roles=("faculty" "admin" "student" "ta")

# Loop through each role and create a curl command
for role in "${roles[@]}"; do
  echo "curl -X 'POST' \\
  'http://localhost:8000/users/' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d ' {
  \"id\": 1,
  \"username\": \"$role\",
  \"password\": \"$role\",
  \"role\": \"$role\"
}' " >> "$temp_file"
  echo "" >> "$temp_file"
done

# Execute the generated curl commands
bash "$temp_file"

# Clean up temporary file
rm "$temp_file"