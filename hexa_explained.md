# Explanation of `hexa.py`

This document provides a detailed explanation of the `hexa.py` script, breaking down each function and major code block to clarify its purpose and functionality.

## Table of Contents
1. [Shebang and Imports](#shebang-and-imports)
2. [`get_config_path`](#get_config_path)
3. [`get_password_hash`](#get_password_hash)
4. [`set_password`](#set_password)
5. [`to_hex` and `from_hex`](#to_hex-and-from_hex)
6. [`process_file`](#process_file)
7. [`main`](#main)
8. [`if __name__ == "__main__"` Block](#if-__name__---__main__-block)

---

### Shebang and Imports

```python
#!/usr/bin/env python3

import sys
import os
import hashlib
import getpass
from configparser import ConfigParser
```

- `#!/usr/bin/env python3`: This is a shebang line that specifies the script should be run with the `python3` interpreter.
- `import sys`: This module provides access to system-specific parameters and functions, such as the command-line arguments (`sys.argv`).
- `import os`: This module provides a way of using operating system-dependent functionality, such as file and directory manipulation.
- `import hashlib`: This module implements a common interface to many different secure hash and message digest algorithms.
- `import getpass`: This module provides a way to securely read a password from the user without echoing it to the terminal.
- `from configparser import ConfigParser`: This module provides a class for working with configuration files in a format similar to INI files.

---

### `get_config_path`

```python
def get_config_path():
    return os.path.join(os.path.expanduser("~"), ".hexa_config")
```

This function returns the full path to the configuration file, which is named `.hexa_config` and stored in the user's home directory.

---

### `get_password_hash`

```python
def get_password_hash():
    config = ConfigParser()
    config.read(get_config_path())
    return config.get("security", "password_hash", fallback=None)
```

This function reads the configuration file and retrieves the stored password hash. If the hash is not found, it returns `None`.

---

### `set_password`

```python
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
```

This function prompts the user to enter and confirm a new password. It then computes the SHA-256 hash of the password, saves it to the configuration file, and sets the file permissions to be readable and writable only by the owner.

---

### `to_hex` and `from_hex`

```python
def to_hex(s):
    return s.encode().hex()

def from_hex(s):
    return bytes.fromhex(s).decode()
```

- `to_hex(s)`: This function takes a string `s`, encodes it into bytes, and then converts the bytes into a hexadecimal string representation.
- `from_hex(s)`: This function takes a hexadecimal string `s`, converts it back into bytes, and then decodes the bytes into a string.

---

### `process_file`

```python
def process_file(file_path, direction):
    # ... (file processing logic)
```

This function handles the conversion of a file's content to or from hexadecimal. It takes the `file_path` and a `direction` (either `"to_hex"` or `"from_hex"`) as input.

- If `direction` is `"to_hex"`, it reads the file, applies the `to_hex` function twice to the content, and overwrites the file with the resulting double-hexadecimal string.
- If `direction` is `"from_hex"`, it first checks if a password is set. If so, it prompts the user for the password, verifies it against the stored hash, and if correct, reads the file, decodes the content using `from_hex` twice, and overwrites the file with the original text.

---

### `main`

```python
def main():
    # ... (main logic)
```

This is the main function of the script. It parses the command-line arguments to determine which command to execute (`hexa`, `unhexa`, or `setpass`). It also ensures that the correct number of arguments is provided and that the file being processed has a `.md` extension.

---

### `if __name__ == "__main__"` Block

```python
if __name__ == "__main__":
    try:
        import termios
    except ImportError:
        pass # termios is not available on all platforms
    main()
```

This block ensures that the `main()` function is called only when the script is executed directly. It also attempts to import the `termios` module, which is used by `getpass` for secure password entry, but passes silently if the import fails (as `termios` is not available on all platforms, such as Windows).
