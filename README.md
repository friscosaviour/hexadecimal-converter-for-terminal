# Hexa - a tool for double hexadecimal conversion

This tool allows you to convert the content of `.md` files to a double hexadecimal format and back to the original text. The conversion back to text is password protected.

## Installation

1.  **Run the installation script:**

    ```bash
    ./install.sh
    ```

2.  **The script will output three commands that you need to run with `sudo`. Copy and paste these commands into your terminal. They will look like this:**

    ```bash
    sudo ln -sf "/path/to/your/hexadecimal/hexa.py" /usr/local/bin/hexa
    sudo ln -sf "/path/to/your/hexadecimal/hexa.py" /usr/local/bin/unhexa
    sudo ln -sf "/path/to/your/hexadecimal/hexa.py" /usr/local/bin/setpass
    ```

3.  **Set your password:**

    After running the `sudo` commands, you need to set a password for decryption. Run the following command and follow the prompts:

    ```bash
    setpass
    ```

## Usage

### `setpass`

Use this command to set or change your password.

```bash
setpass
```

### `hexa`

This command converts the content of a `.md` file to double hexadecimal format. The original file will be overwritten.

```bash
hexa <file.md>
```

**Example:**

```bash
hexa my_document.md
```

### `unhexa`

This command converts a double hexadecimal `.md` file back to its original text. You will be prompted for your password.

```bash
unhexa <file.md>
```

**Example:**

```bash
unhexa my_document.md
```

## How it works

The `hexa` command takes the content of your `.md` file, converts it to a hexadecimal string, and then converts that hexadecimal string to hexadecimal again. The `unhexa` command reverses this process.

The password you set with `setpass` is stored as a SHA256 hash in a configuration file in your home directory (`~/.hexa_config`). This file is protected with read/write permissions for your user only.
