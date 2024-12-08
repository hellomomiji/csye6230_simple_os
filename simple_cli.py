import cmd
from simple_kernel import Kernel
from simple_fs import FileSystem
import random

class FileSysCLI(cmd.Cmd):
    """
    Command-line interface for interacting with kernel-integrated file system.
    """
    intro = '''
    Welcome to SimpleOS 
    - Kernel-integrated File System
    - Type help or ? to list commands
    '''
    prompt = 'SimpleOS> '

    def __init__(self):
        super().__init__()
        # Initialize kernel
        self.kernel = Kernel()
        
        # Start kernel services
        self.kernel.start()
        
        # Initialize file system with kernel
        self.filesystem = FileSystem(self.kernel)
    
    def do_help(self, arg: str) -> bool | None:
        """
        Display help message
        """
        print(
            """
            Commands:
            - create filename [content] [memory_size]: Create a new file
            - list: List all files
            - read filename: Read file content
            - remove filename: Remove a file
            - rename old_name new_name: Rename a file
            - memory: Display memory status
            - exit: Exit the CLI
            """
        )

        
    
    def do_create(self, arg):
        """
        Create a new file: create filename [content]
        Optional: specify memory size for the file
        
        Examples:
        create myfile.txt
        create myfile.txt "Hello, World!"
        create myfile.txt "Large content" 500
        """
        args = arg.split(maxsplit=2)
        
        # Default values
        filename = args[0]
        content = args[1] if len(args) > 1 else ''
        memory_size = int(args[2]) if len(args) > 2 else 100
        
        # Use kernel-integrated file system creation
        process_id = self.filesystem.create_file(
            filename, 
            content, 
            memory_required=memory_size
        )
        
        if process_id:
            print(f"[Log] File created with process ID: {process_id}")
    
    def do_list(self, arg):
        """List all files in the file system: list"""
        files = self.filesystem.list_files()
        print("Files:")
        for file in files:
            file_content = self.filesystem.read_file(file)
            print(f"- {file} (Size: {len(file_content)} bytes)")
    
    def do_read(self, arg):
        """Read file content: read filename"""
        content = self.filesystem.read_file(arg)
        if content is not None:
            print(f"[Log] Content of {arg}:\n{content}")
        else:
            print(f"[Error] File '{arg}' not found.")
    
    def do_remove(self, arg):
        """Remove a file: remove filename"""
        process_id = self.filesystem.remove_file(arg)
        if process_id:
            print(f"[Log] File '{arg}' removed with process ID: {process_id}")
        else:
            print(f"[Error] File '{arg}' not found.")
    
    def do_rename(self, arg):
        """Rename a file: rename old_name new_name"""
        args = arg.split()
        if len(args) != 2:
            print("[Error] Usage: rename old_name new_name")
            return
        
        old_name, new_name = args
        if self.filesystem.rename_file(old_name, new_name):
            print(f"[Log] File renamed from '{old_name}' to '{new_name}' successfully.")
        else:
            print(f"[Error] Failed to rename file. Check if '{old_name}' exists or '{new_name}' is already taken.")
    
    def do_memory(self, arg):
        """
        Display current memory status
        """
        memory_manager = self.kernel.memory_manager
        print(f"Total Memory: {memory_manager.total_memory} bytes")
        print(f"Used Memory: {memory_manager.used_memory} bytes")
        print(f"Free Memory: {memory_manager.get_free_memory()} bytes")
    
    def do_exit(self, arg):
        """Exit the CLI and stop kernel services: exit"""
        self.kernel.stop()
        return True

def main():
    cli = FileSysCLI()
    cli.cmdloop()

if __name__ == '__main__':
    main()

# # Example usage script
# def demonstrate_filesystem():
#     """
#     Demonstrate advanced file system capabilities with kernel integration
#     """
#     kernel = Kernel()
#     kernel.start()
    
#     filesystem = FileSystem(kernel)
    
#     # Create files with different memory requirements
#     filesystem.create_file("small.txt", "Small file", memory_required=50)
#     filesystem.create_file("medium.txt", "Medium-sized file content", memory_required=200)
#     filesystem.create_file("large.txt", "A" * 1000, memory_required=500)
    
#     # List and read files
#     print("Files:", filesystem.list_files())
    
#     # Stop kernel
#     kernel.stop()

# if __name__ == '__main__':
#     demonstrate_filesystem()