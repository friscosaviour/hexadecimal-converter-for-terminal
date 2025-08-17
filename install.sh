#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Make the python script executable
chmod +x "$SCRIPT_DIR/hexa.py"

# Instructions for the user
echo "Please run the following commands to complete the installation:"
echo "sudo ln -sf \"$SCRIPT_DIR/hexa.py\" /usr/local/bin/hexa"
echo "sudo ln -sf \"$SCRIPT_DIR/hexa.py\" /usr/local/bin/unhexa"
echo "sudo ln -sf \"$SCRIPT_DIR/hexa.py\" /usr/local/bin/setpass"

echo "\nAfter running the commands, you can set your password by running:"
echo "setpass"