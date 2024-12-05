#!/bin/bash

# Simple OS Command-Line Interface
# Requires Python and the SimpleOS script to be in the same directory

# Configuration
PYTHON_SCRIPT="simple_os.py"
FILESYSTEM_DIR="filesystem"

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Help function to display available commands
show_help() {
    echo -e "${YELLOW}Simple OS CLI Help${NC}"
    echo "Usage: ./os_cli.sh [COMMAND] [ARGUMENTS]"
    echo ""
    echo "Available Commands:"
    echo "  create  <filename> [content]  - Create a new file"
    echo "  list                          - List all files"
    echo "  read    <filename>            - Read file contents"
    echo "  remove  <filename>            - Remove a file"
    echo "  rename  <old_name> <new_name> - Rename a file"
    echo "  help                          - Show this help message"
}

# Validate that Python script exists
validate_python_script() {
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        echo -e "${RED}Error: Python script $PYTHON_SCRIPT not found!${NC}"
        exit 1
    fi
}

# Create a file
create_file() {
    validate_python_script
    
    if [ $# -lt 1 ]; then
        echo -e "${RED}Error: Filename required${NC}"
        exit 1
    fi
    
    filename="$1"
    shift
    content="$*"
    
    python3 "$PYTHON_SCRIPT" create "$filename" "$content"
}

# List files
list_files() {
    validate_python_script
    python3 "$PYTHON_SCRIPT" list
}

# Read file contents
read_file() {
    validate_python_script
    
    if [ $# -ne 1 ]; then
        echo -e "${RED}Error: Filename required${NC}"
        exit 1
    fi
    
    python3 "$PYTHON_SCRIPT" read "$1"
}

# Remove a file
remove_file() {
    validate_python_script
    
    if [ $# -ne 1 ]; then
        echo -e "${RED}Error: Filename required${NC}"
        exit 1
    fi
    
    python3 "$PYTHON_SCRIPT" remove "$1"
}

# Rename a file
rename_file() {
    validate_python_script
    
    if [ $# -ne 2 ]; then
        echo -e "${RED}Error: Old and new filenames required${NC}"
        exit 1
    fi
    
    python3 "$PYTHON_SCRIPT" rename "$1" "$2"
}

# Main CLI logic
main() {
    # Ensure filesystem directory exists
    mkdir -p "$FILESYSTEM_DIR"

    # Parse commands
    case "$1" in
        create)
            shift
            create_file "$@"
            ;;
        list)
            list_files
            ;;
        read)
            shift
            read_file "$@"
            ;;
        remove)
            shift
            remove_file "$@"
            ;;
        rename)
            shift
            rename_file "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Invalid command. Use 'help' for usage information.${NC}"
            exit 1
            ;;
    esac
}

# Run the main function with all arguments
main "$@"
