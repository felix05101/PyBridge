import subprocess
import sys
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def run_command(command, check=True):
    """Run a system command and print its output."""
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}", file=sys.stderr)
        return e  # Return the exception for further handling

def clear_console():
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def install_bridge_utils():
    """Ensure bridge-utils is installed."""
    try:
        subprocess.run(['dpkg', '-l', '|', 'grep', '-q', 'bridge-utils'], check=True, shell=True)
        print("bridge-utils is already installed.")
    except subprocess.CalledProcessError:
        print("Installing bridge-utils...")
        run_command(['sudo', 'apt', 'update'])
        run_command(['sudo', 'apt', 'install', '-y', 'bridge-utils'])

def list_bridges():
    """List all existing bridges."""
    try:
        output = run_command(['brctl', 'show'], check=False).stdout
        if not output.strip():
            print("No bridges found.")
            return []
        bridges = [line.split()[0] for line in output.splitlines()[1:] if line]
        return bridges
    except subprocess.CalledProcessError:
        print("Failed to list bridges.")
        return []

def list_interfaces():
    """List all network interfaces."""
    try:
        output = run_command(['ip', 'link', 'show'], check=False).stdout
        interfaces = [line.split(':')[1].strip() for line in output.splitlines() if ':' in line]
        return interfaces
    except subprocess.CalledProcessError:
        print("Failed to list interfaces.")
        return []

def create_bridge(bridge_name, interfaces):
    """Create a new bridge if it does not already exist."""
    bridges = list_bridges()
    if bridge_name in bridges:
        print(f"Bridge {bridge_name} already exists.")
        return False
    print(f"Creating bridge {bridge_name}...")
    run_command(['sudo', 'brctl', 'addbr', bridge_name])
    run_command(['sudo', 'ip', 'link', 'set', 'dev', bridge_name, 'up'])
    add_interfaces_to_bridge(bridge_name, interfaces)
    set_interfaces_down_up(interfaces)
    return True

def add_interfaces_to_bridge(bridge_name, interfaces):
    """Add interfaces to the specified bridge."""
    for iface in interfaces:
        if subprocess.run(['ip', 'link', 'show', iface], capture_output=True, text=True).returncode == 0:
            print(f"Adding interface {iface} to bridge {bridge_name}...")
            run_command(['sudo', 'brctl', 'addif', bridge_name, iface], check=False)
        else:
            print(f"Interface {iface} does not exist; skipping.")

def set_interfaces_down_up(interfaces):
    """Bring interfaces down and then up."""
    for iface in interfaces:
        if subprocess.run(['ip', 'link', 'show', iface], capture_output=True, text=True).returncode == 0:
            print(f"Bringing interface {iface} down...")
            run_command(['sudo', 'ip', 'link', 'set', 'dev', iface, 'down'])
            print(f"Bringing interface {iface} up...")
            run_command(['sudo', 'ip', 'link', 'set', 'dev', iface, 'up'])
        else:
            print(f"Interface {iface} does not exist; not bringing it down/up.")

def bring_down_bridge(bridge_name):
    """Bring down the bridge."""
    print(f"Bringing down bridge {bridge_name}...")
    run_command(['sudo', 'ip', 'link', 'set', 'dev', bridge_name, 'down'])

def remove_interfaces_from_bridge(bridge_name):
    """Remove all interfaces from the bridge."""
    output = run_command(['brctl', 'show', bridge_name], check=False).stdout
    lines = output.splitlines()
    interfaces = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) > 1:
            interface = parts[1]
            interfaces.append(interface)
    for iface in interfaces:
        print(f"Removing interface {iface} from bridge {bridge_name}...")
        result = run_command(['sudo', 'brctl', 'delif', bridge_name, iface], check=False)
        if result.returncode != 0:
            print(f"Failed to remove interface {iface} from bridge {bridge_name}: {result.stderr.strip()}")

def delete_bridge(bridge_name):
    """Delete an existing bridge."""
    bridges = list_bridges()
    if not bridges:
        print("No bridges to delete.")
        return
    if bridge_name not in bridges:
        print(f"Bridge {bridge_name} does not exist.")
        return

    # Bring down the bridge
    bring_down_bridge(bridge_name)
    
    # Remove interfaces from the bridge
    remove_interfaces_from_bridge(bridge_name)
    
    # Finally, delete the bridge
    print(f"Deleting bridge {bridge_name}...")
    run_command(['sudo', 'brctl', 'delbr', bridge_name])
    print("Bridge deleted.")

def handle_create_bridge():
    """Handle creating a new bridge."""
    interfaces = list_interfaces()
    if not interfaces:
        print("No network interfaces found.")
        return

    clear_console()
    print(Fore.CYAN + "Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(Fore.YELLOW + f"{i + 1}: {iface}")

    bridge_name = input(Fore.GREEN + "Enter the name of the bridge to create: ").strip()
    num_interfaces = int(input(Fore.GREEN + "How many interfaces do you want to add (2)? "))

    if num_interfaces != 2:
        print(Fore.RED + "You must select exactly 2 interfaces.")
        return

    chosen_interfaces = []
    for i in range(num_interfaces):
        choice = int(input(Fore.GREEN + f"Enter the number of interface {i + 1}: ")) - 1
        if 0 <= choice < len(interfaces):
            chosen_interfaces.append(interfaces[choice])
        else:
            print(Fore.RED + f"Invalid choice: {choice + 1}.")
            return

    if create_bridge(bridge_name, chosen_interfaces):
        print(Fore.GREEN + "Bridge setup completed.")
    else:
        print(Fore.RED + "Failed to create bridge.")

def handle_delete_bridge():
    """Handle deleting an existing bridge."""
    bridges = list_bridges()
    if not bridges:
        print(Fore.RED + "No bridges to delete.")
        return

    clear_console()
    print(Fore.CYAN + "Existing bridges:")
    for i, bridge in enumerate(bridges):
        print(Fore.YELLOW + f"{i + 1}: {bridge}")

    bridge_number = int(input(Fore.GREEN + "Enter the number of the bridge to delete: ")) - 1
    if 0 <= bridge_number < len(bridges):
        bridge_name = bridges[bridge_number]
        delete_bridge(bridge_name)
    else:
        print(Fore.RED + "Invalid bridge number.")

def main_menu():
    """Display the main menu and handle user actions."""
    while True:
        clear_console()
        print(Fore.MAGENTA + "HypexTRADEMARK" + Style.RESET_ALL)
        action = input(Fore.CYAN + "\nWould you like to (C)reate a new bridge, (D)elete an existing bridge, or (Q)uit? ").strip().upper()
        if action == 'C':
            handle_create_bridge()
        elif action == 'D':
            handle_delete_bridge()
        elif action == 'Q':
            print(Fore.GREEN + "Exiting.")
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid action. Please choose 'C', 'D', or 'Q'.")

def main():
    if not subprocess.run(['id', '-u'], capture_output=True, text=True).stdout.strip() == '0':
        print(Fore.RED + "Please run as root (use sudo).")
        sys.exit(1)

    install_bridge_utils()
    main_menu()

if __name__ == "__main__":
    main()
