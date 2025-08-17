#!/usr/bin/env python3

import sys
import os
import hashlib
import getpass
from configparser import ConfigParser

def get_config_path():
    return os.path.join(os.path.expanduser("~"), ".hexa_config")

def get_password_hash():
    config = ConfigParser()
    config.read(get_config_path())
    return config.get("security", "password_hash", fallback=None)

def set_password():
    config = ConfigParser()
    config_path = get_config_path()
    
    while True:
        try:
            password = getpass.getpass("Enter a new password: ")
            password_confirm = getpass.getpass("Confirm new password: ")
            if password == password_confirm:
                break
            else:
                print("Passwords do not match. Please try again.")
        except (EOFError, termios.error):
            print("Could not read password. Are you running in an interactive terminal?")
            return

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    config["security"] = {"password_hash": password_hash}
    with open(config_path, "w") as f:
        config.write(f)
    os.chmod(config_path, 0o600)  # Set permissions to read/write for owner only
    print("Password set successfully.")

def to_hex(s):
    return s.encode().hex()

def from_hex(s):
    return bytes.fromhex(s).decode()

def process_file(file_path, direction):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    if direction == "to_hex":
        with open(file_path, "r+") as f:
            content = f.read()
            hex_content = to_hex(to_hex(content))
            f.seek(0)
            f.write(hex_content)
            f.truncate()
        print(f"Successfully converted {file_path} to double hexadecimal.")
    elif direction == "from_hex":
        password_hash = get_password_hash()
        if not password_hash:
            print("No password set. Please run 'setpass' to set a password first.")
            return

        try:
            password = getpass.getpass("Enter password to decrypt: ")
        except (EOFError, termios.error):
            print("Could not read password. Are you running in an interactive terminal?")
            return

        if hashlib.sha256(password.encode()).hexdigest() != password_hash:
            print("Incorrect password.")
            return

        with open(file_path, "r+") as f:
            content = f.read()
            try:
                original_content = from_hex(from_hex(content))
                f.seek(0)
                f.write(original_content)
                f.truncate()
                print(f"Successfully converted {file_path} back to original text.")
            except (ValueError, TypeError):
                print(f"Error: The content of {file_path} does not appear to be in the correct hexadecimal format.")

def main():
    if len(sys.argv) < 2 and os.path.basename(sys.argv[0]) not in ("setpass",):
        print("Usage: hexa <file.md> | unhexa <file.md> | setpass")
        return

    command = os.path.basename(sys.argv[0])
    
    if command == "setpass" or (len(sys.argv) > 1 and sys.argv[1] == "setpass"):
        set_password()
        return

    if len(sys.argv) != 2:
        print(f"Usage: {command} <file.md>")
        return

    file_path = sys.argv[1]

    if not file_path.endswith(".md"):
        print("This tool only supports .md files.")
        return

    if command == "hexa":
        process_file(file_path, "to_hex")
    elif command == "unhexa":
        process_file(file_path, "from_hex")
    else:
        print(f"Unknown command: {command}. Try 'hexa', 'unhexa', or 'setpass'.")

if __name__ == "__main__":
    try:
        import termios
    except ImportError:
        pass # termios is not available on all platforms
    main()