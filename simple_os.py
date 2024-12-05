import os
import sys
import shutil

class SimpleOS:
    def __init__(self, base_path: str = "filesystem"):
        """
        Initialize the simple operating system with a base file system directory
        
        Args:
            base_path (str): Root directory for the file system
        """
        self.base_path = os.path.abspath(base_path)
        
        # Create base directory if it doesn't exist
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def create_file(self, filename: str, content: str = "") -> bool:
        """
        Create a new file in the file system
        
        Args:
            filename (str): Name of the file to create
            content (str, optional): Initial content of the file
        
        Returns:
            bool: True if file created successfully, False otherwise
        """
        try:
            filepath = os.path.join(self.base_path, filename)
            
            # Prevent directory traversal attacks
            if os.path.commonpath([self.base_path, filepath]) != self.base_path:
                print(f"Error: Invalid filename {filename}")
                return False
            
            with open(filepath, 'w') as file:
                file.write(content)
            print(f"File {filename} created successfully")
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def list_files(self) -> None:
        """
        List all files in the file system
        """
        try:
            files = [f for f in os.listdir(self.base_path) 
                     if os.path.isfile(os.path.join(self.base_path, f))]
            if files:
                for file in files:
                    print(file)
            else:
                print("No files found.")
        except Exception as e:
            print(f"Error listing files: {e}")
    
    def read_file(self, filename: str) -> bool:
        """
        Read the contents of a file
        
        Args:
            filename (str): Name of the file to read
        
        Returns:
            bool: True if file read successfully, False otherwise
        """
        try:
            filepath = os.path.join(self.base_path, filename)
            
            # Prevent directory traversal attacks
            if os.path.commonpath([self.base_path, filepath]) != self.base_path:
                print(f"Error: Invalid filename {filename}")
                return False
            
            with open(filepath, 'r') as file:
                print(file.read())
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def remove_file(self, filename: str) -> bool:
        """
        Remove a file from the file system
        
        Args:
            filename (str): Name of the file to remove
        
        Returns:
            bool: True if file removed successfully, False otherwise
        """
        try:
            filepath = os.path.join(self.base_path, filename)
            
            # Prevent directory traversal attacks
            if os.path.commonpath([self.base_path, filepath]) != self.base_path:
                print(f"Error: Invalid filename {filename}")
                return False
            
            os.remove(filepath)
            print(f"File {filename} removed successfully")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as e:
            print(f"Error removing file: {e}")
            return False
    
    def rename_file(self, old_filename: str, new_filename: str) -> bool:
        """
        Rename a file in the file system
        
        Args:
            old_filename (str): Current name of the file
            new_filename (str): New name for the file
        
        Returns:
            bool: True if file renamed successfully, False otherwise
        """
        try:
            old_filepath = os.path.join(self.base_path, old_filename)
            new_filepath = os.path.join(self.base_path, new_filename)
            
            # Prevent directory traversal attacks
            if (os.path.commonpath([self.base_path, old_filepath]) != self.base_path or 
                os.path.commonpath([self.base_path, new_filepath]) != self.base_path):
                print(f"Error: Invalid filename")
                return False
            
            shutil.move(old_filepath, new_filepath)
            print(f"File renamed from {old_filename} to {new_filename}")
            return True
        except FileNotFoundError:
            print(f"File {old_filename} not found")
            return False
        except Exception as e:
            print(f"Error renaming file: {e}")
            return False

def main():
    # Create SimpleOS instance
    file_system = SimpleOS()
    
    # Check if correct number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python simple_os.py [create|list|read|remove|rename] [arguments]")
        sys.exit(1)
    
    # Parse commands
    command = sys.argv[1]
    
    try:
        if command == 'create':
            if len(sys.argv) < 3:
                print("Usage: python simple_os.py create <filename> [content]")
                sys.exit(1)
            filename = sys.argv[2]
            content = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            file_system.create_file(filename, content)
        
        elif command == 'list':
            file_system.list_files()
        
        elif command == 'read':
            if len(sys.argv) != 3:
                print("Usage: python simple_os.py read <filename>")
                sys.exit(1)
            file_system.read_file(sys.argv[2])
        
        elif command == 'remove':
            if len(sys.argv) != 3:
                print("Usage: python simple_os.py remove <filename>")
                sys.exit(1)
            file_system.remove_file(sys.argv[2])
        
        elif command == 'rename':
            if len(sys.argv) != 4:
                print("Usage: python simple_os.py rename <old_filename> <new_filename>")
                sys.exit(1)
            file_system.rename_file(sys.argv[2], sys.argv[3])
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()