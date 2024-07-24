# Bridge Management Script

This Python script provides a command-line utility to manage network bridges on a Linux system. It allows users to create, delete, and list network bridges, as well as manage their associated interfaces. The script utilizes `colorama` for color-coded output and `subprocess` to execute system commands.

## Features

- **Create a Bridge:** Create a new network bridge with specified interfaces.
- **Delete a Bridge:** Remove an existing network bridge.
- **List Bridges:** View all existing network bridges.
- **List Interfaces:** View all available network interfaces.
- **Handle Interfaces:** Add and remove network interfaces from bridges.

## Requirements

- Python 3
- `colorama` library
- `bridge-utils` package (automatically installed if missing)

## Installation

1. Clone the repository or download the script.

2. Navigate to the directory where the script is located.

3. Create a `requirements.txt` file with the following content:

    ```
    colorama
    ```

4. Install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

5. Ensure you have `bridge-utils` installed. The script will attempt to install it if it's not present.

## Usage

1. **Run the Script:**
   
   Execute the script with root privileges:

    ```bash
    sudo python3 bridge_manager.py
    ```

2. **Main Menu:**

   - **(C)reate**: Create a new bridge.
   - **(D)elete**: Delete an existing bridge.
   - **(Q)uit**: Exit the script.

3. **Creating a Bridge:**
   
   - List available network interfaces.
   - Select exactly 2 interfaces to add to the new bridge.
   - Provide a name for the new bridge.

4. **Deleting a Bridge:**
   
   - List existing bridges.
   - Select the bridge to delete.

## Functions

- `run_command(command, check=True)`: Runs a system command and prints the output.
- `clear_console()`: Clears the console screen.
- `install_bridge_utils()`: Ensures `bridge-utils` is installed.
- `list_bridges()`: Lists all existing network bridges.
- `list_interfaces()`: Lists all network interfaces.
- `create_bridge(bridge_name, interfaces)`: Creates a new bridge with specified interfaces.
- `add_interfaces_to_bridge(bridge_name, interfaces)`: Adds interfaces to the specified bridge.
- `set_interfaces_down_up(interfaces)`: Brings interfaces down and then up.
- `bring_down_bridge(bridge_name)`: Brings down the specified bridge.
- `remove_interfaces_from_bridge(bridge_name)`: Removes all interfaces from the bridge.
- `delete_bridge(bridge_name)`: Deletes the specified bridge.
- `handle_create_bridge()`: Handles the creation of a new bridge.
- `handle_delete_bridge()`: Handles the deletion of an existing bridge.
- `main_menu()`: Displays the main menu and handles user actions.
- `main()`: Entry point of the script.

## Notes

- Ensure you have the necessary permissions to modify network configurations.
- This script is designed to work on Linux systems with `bridge-utils` installed.

## License

This script is provided as-is. Use it at your own risk. For any modifications or contributions, please follow the standard open-source practices.

---

Feel free to modify and extend this script according to your requirements. For any issues or questions, open an issue in the repository.
