# SUBTASK-T003.md - Error Handling in Installation Scripts

## Parent Task
**T003**: Enhance error handling in installation scripts

## Specific Goal
Improve the reliability and user experience of the installation process by implementing robust error handling, user feedback, and recovery mechanisms in the installation scripts.

## Dependencies
None

## Implementation Approach

The improved error handling will follow these key principles:
1. Graceful failure with informative error messages
2. Prerequisite checking before execution
3. Progress feedback during lengthy operations
4. Recovery suggestions when errors occur
5. Comprehensive logging of installation steps

## Progress Status: 0%

## Validation Criteria
- All required dependencies are checked before installation begins
- Each installation step provides clear feedback on progress
- Errors are caught and displayed with actionable information
- Installation logs are created for troubleshooting
- Failed installations can be resumed or safely retried
- Error messages are user-friendly and include resolution steps

## Files to Modify

### Primary Files
- `install.py` - Main Python installation script
- `install.sh` - Shell wrapper for the installation script

### Supporting Files
- Create `install_utils.py` - Helper functions for installation process
- Create `install_logger.py` - Dedicated logger for installation process

## Implementation Details

### 1. Prerequisites Check Function

```python
# install_utils.py - Prerequisites checking function
import os
import platform
import shutil
import subprocess
import sys

def check_prerequisites():
    """
    Check all prerequisites for installation and return list of issues
    
    Returns:
        tuple: (is_valid, issues)
            is_valid (bool): True if all prerequisites are met
            issues (list): List of issues that need to be resolved
    """
    issues = []
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        issues.append(f"Python 3.6+ required, found {python_version.major}.{python_version.minor}")
    
    # Check operating system
    if platform.system() != "Linux":
        issues.append(f"This script is designed to run on Linux, found {platform.system()}")
        
    # Specifically check for Kali Linux
    try:
        with open('/etc/os-release', 'r') as file:
            content = file.read()
            if "kali" not in content.lower():
                issues.append("This script is designed for Kali Linux")
    except FileNotFoundError:
        issues.append("Unable to determine Linux distribution")
    
    # Check for required commands
    required_commands = ["git", "docker", "curl", "wget"]
    missing_commands = []
    
    for cmd in required_commands:
        if shutil.which(cmd) is None:
            missing_commands.append(cmd)
    
    if missing_commands:
        issues.append(f"Missing required commands: {', '.join(missing_commands)}")
    
    # Check for required system packages
    required_packages = ["python3-pip", "build-essential"]
    
    try:
        # Try using dpkg to check installed packages
        for pkg in required_packages:
            result = subprocess.run(
                ["dpkg", "-s", pkg], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                check=False
            )
            if result.returncode != 0:
                issues.append(f"Required package not installed: {pkg}")
    except Exception:
        issues.append("Unable to check for required system packages")
    
    # Check for disk space (at least 5GB free)
    try:
        disk_usage = shutil.disk_usage(".")
        free_gb = disk_usage.free / (1024**3)
        if free_gb < 5:
            issues.append(f"Insufficient disk space: {free_gb:.1f}GB free, 5GB required")
    except Exception:
        issues.append("Unable to check available disk space")
    
    # Check for internet connectivity
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode != 0:
            issues.append("No internet connectivity detected")
    except Exception:
        issues.append("Unable to check internet connectivity")
    
    return len(issues) == 0, issues
```

### 2. Enhanced Error Handling in install.py

```python
# Key sections to update in install.py

import sys
import traceback
import time
import os
from install_logger import setup_logger
from install_utils import check_prerequisites

# Setup logger
logger = setup_logger()

def main():
    """
    Main installation function with enhanced error handling
    """
    try:
        # Clear screen and show welcome message
        clear_screen()
        print_banner()
        
        # Log start of installation
        logger.info("Starting Ars0n Framework installation")
        
        # Check prerequisites
        logger.info("Checking prerequisites...")
        prerequisites_met, issues = check_prerequisites()
        
        if not prerequisites_met:
            logger.error("Prerequisite check failed")
            print("\n\033[91mPrerequisite Check Failed\033[0m")
            print("The following issues need to be resolved before installation:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
            
            print("\nSuggested actions:")
            print("1. Ensure you're running on a clean Kali Linux installation")
            print("2. Run 'apt update && apt upgrade' to update your system")
            print("3. Install missing packages with 'apt install <package>'")
            
            user_choice = input("\nDo you want to attempt installation anyway? (y/N): ").strip().lower()
            if user_choice != 'y':
                logger.info("User aborted installation after prerequisite check")
                sys.exit(1)
            logger.warning("User proceeding despite prerequisite failures")
        
        # Create progress tracker
        total_steps = 7  # Total number of installation steps
        current_step = 0
        
        # Step 1: Update system
        current_step += 1
        print_progress("Updating system packages", current_step, total_steps)
        logger.info("Updating system packages")
        try:
            run_command("sudo apt update")
            run_command("sudo apt -y upgrade")
        except CommandError as e:
            logger.error(f"System update failed: {str(e)}")
            handle_error("System update failed", str(e), [
                "Try updating manually with: sudo apt update && sudo apt -y upgrade",
                "Check your internet connection",
                "Ensure you have sudo privileges"
            ])
        
        # Continue with additional steps...
        # Each step should follow the pattern:
        # 1. Increment step counter
        # 2. Print progress
        # 3. Log step
        # 4. Try to execute step
        # 5. Catch specific errors and provide recovery suggestions
        
        # ...
        
        # Installation complete
        logger.info("Installation completed successfully")
        print("\n\033[92mArs0n Framework installed successfully!\033[0m")
        print("You can now run the framework with: ./run.sh\n")
        
    except KeyboardInterrupt:
        logger.warning("Installation interrupted by user")
        print("\n\033[93mInstallation interrupted by user\033[0m")
        print("Cleaning up...")
        # Perform cleanup if needed
        sys.exit(1)
    except Exception as e:
        # Catch any unhandled exceptions
        logger.error(f"Unhandled exception during installation: {str(e)}")
        logger.error(traceback.format_exc())
        print("\n\033[91mUnexpected error during installation\033[0m")
        print(f"Error details: {str(e)}")
        print("\nA detailed log has been saved to: ./install.log")
        print("Please include this log if you report this issue.")
        sys.exit(1)

def run_command(command, error_msg=None):
    """
    Run a shell command with error handling
    
    Args:
        command (str): Command to run
        error_msg (str, optional): Custom error message. Defaults to None.
    
    Raises:
        CommandError: If command fails
    """
    logger.info(f"Running command: {command}")
    result = subprocess.run(
        command, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    
    if result.returncode != 0:
        log_msg = f"Command failed: {command}"
        if result.stderr:
            log_msg += f"\nError: {result.stderr}"
        
        logger.error(log_msg)
        raise CommandError(error_msg or result.stderr or "Command failed")
    
    return result.stdout

def print_progress(message, current, total):
    """
    Print a progress message with step count
    
    Args:
        message (str): Message to display
        current (int): Current step number
        total (int): Total number of steps
    """
    percentage = int((current / total) * 100)
    progress_bar = "[" + "#" * (percentage // 5) + " " * (20 - (percentage // 5)) + "]"
    print(f"\n\033[94m{progress_bar} {percentage}% - Step {current}/{total}\033[0m")
    print(f"\033[1m{message}\033[0m")

def handle_error(title, message, suggestions=None):
    """
    Handle an error with helpful suggestions
    
    Args:
        title (str): Error title
        message (str): Error details
        suggestions (list, optional): List of suggestions to fix the issue
    """
    print(f"\n\033[91m{title}\033[0m")
    print(f"Error details: {message}")
    
    if suggestions:
        print("\nTry the following:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    user_choice = input("\nDo you want to continue with the installation? (y/N): ").strip().lower()
    if user_choice != 'y':
        logger.info("User aborted installation after error")
        sys.exit(1)
    
    logger.warning("User continuing installation despite error")

class CommandError(Exception):
    """Exception raised when a command fails"""
    pass

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')

def print_banner():
    """Print Ars0n Framework installation banner"""
    banner = """
    █████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
   ██╔══██╗██╔══██╗██╔════╝██╔═████╗████╗  ██║
   ███████║██████╔╝███████╗██║██╔██║██╔██╗ ██║
   ██╔══██║██╔══██╗╚════██║████╔╝██║██║╚██╗██║
   ██║  ██║██║  ██║███████║╚██████╔╝██║ ╚████║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
   
   Framework Installation - v0.0.2-alpha
    """
    print("\033[95m" + banner + "\033[0m")

if __name__ == "__main__":
    main()
```

### 3. Installation Logger

```python
# install_logger.py
import logging
import os
import sys
from datetime import datetime

def setup_logger():
    """
    Set up a logger for the installation process
    
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logger
    logger = logging.getLogger('ars0n_installer')
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Log format
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create file handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'logs/install_{timestamp}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # Create console handler (less verbose)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    return logger
```

### 4. Enhanced Shell Wrapper (install.sh)

```bash
#!/bin/bash

# Error handling
set -e

# Variables
LOGFILE="./logs/install_shell.log"
PYTHON_SCRIPT="install.py"

# Create logs directory if it doesn't exist
mkdir -p logs

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"
}

# Error handler
error_handler() {
    log "ERROR: Installation failed at line $1"
    echo ""
    echo "Installation failed. Please check the logs at $LOGFILE for details."
    echo "For support, please visit: https://github.com/R-s0n/ars0n-framework/issues"
    exit 1
}

# Set up error handling
trap 'error_handler $LINENO' ERR

# Start installation
log "Starting Ars0n Framework installation"

# Check Python version
if ! command -v python3 &> /dev/null; then
    log "Python 3 not found. Installing..."
    apt update && apt install -y python3 python3-pip
fi

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Check ARM architecture
ARM_FLAG=""
if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "armv7l" ]; then
    log "ARM architecture detected"
    ARM_FLAG="--arm"
fi

# Run the Python installation script
log "Running Python installation script..."
python3 "$PYTHON_SCRIPT" $ARM_FLAG

# Check if installation was successful
if [ $? -eq 0 ]; then
    log "Installation completed successfully"
    
    # Ask if user wants to run the application now
    echo ""
    echo "Do you want to run the Ars0n Framework now? (y/N)"
    read -r run_now
    
    if [[ $run_now =~ ^[Yy]$ ]]; then
        log "Starting Ars0n Framework..."
        ./run.sh $ARM_FLAG
    else
        echo ""
        echo "You can run the framework later using:"
        echo "./run.sh $ARM_FLAG"
    fi
else
    log "Installation failed"
    echo ""
    echo "Installation failed. Please check the logs at $LOGFILE for details."
    echo "For support, please visit: https://github.com/R-s0n/ars0n-framework/issues"
    exit 1
fi
```

## Remaining Tasks

1. Update install.py with error handling
   - Add prerequisites checking
   - Add progress reporting
   - Add error recovery suggestions
   - Status: Not Started

2. Create install_utils.py
   - Implement prerequisite checks
   - Implement command wrapper
   - Status: Not Started

3. Create install_logger.py
   - Implement installer logging
   - Status: Not Started

4. Update install.sh
   - Add error handling
   - Add better detection for ARM architecture
   - Add logging
   - Status: Not Started

5. Testing
   - Test on clean Kali Linux installation
   - Test with missing dependencies
   - Test with interrupted installation
   - Status: Not Started 