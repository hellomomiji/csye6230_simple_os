import json
import threading
from typing import Dict, Any, Optional
from simple_kernel import Kernel, Process

class FileSystemProcess(Process):
    def __init__(self, name: str, operation: str):
        """
        Specialized process for file system operations.
        
        :param name: Process name
        :param operation: Type of file system operation
        """
        super().__init__(name, priority=5)  # Medium priority for file operations
        self.operation = operation
        self.result = None
        self.completed = False

class FileSystem:
    def __init__(self, kernel: Kernel, storage_path: str = 'filesystem.json'):
        """
        File system integrated with kernel.
        
        :param kernel: Kernel instance for process and memory management
        :param storage_path: Path to store file system data
        """
        self.kernel = kernel
        self.storage_path = storage_path
        self.files: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.load_filesystem()
    
    def load_filesystem(self):
        """
        Load existing file system from storage.
        Creates a new storage if it doesn't exist.
        """
        try:
            with open(self.storage_path, 'r') as f:
                self.files = json.load(f)
        except FileNotFoundError:
            self.files = {}
            self.files['README.txt'] = {
                'content': 'Welcome to SimpleFS!',
                'size': 20,
                'process_id': None
            }
            self.save_filesystem()
    
    def save_filesystem(self):
        """
        Save current file system state to storage.
        """
        with open(self.storage_path, 'w') as f:
            json.dump(self.files, f, indent=2)
    
    def _create_file_process(self, filename: str, content: str = '') -> FileSystemProcess:
        """
        Create a file system operation process.
        
        :param filename: Name of the file
        :param op: Type of file system operation
        :param content: Content of the file
        :return: FileSystemProcess instance
        """
        process = FileSystemProcess(f"Create file - {filename}", "CREATE")
        process.context = {
            'filename': filename,
            'content': content
        }
        return process 
    
    def _remove_file_process(self, filename: str) -> FileSystemProcess:
        """
        Create a file system operation process.
        
        :param filename: Name of the file
        :return: FileSystemProcess instance
        """
        return FileSystemProcess(f"Remove file - {filename}", "REMOVE")
    
    
    
    def create_file(self, filename: str, content: str = '', memory_required: int = 100) -> Optional[str]:
        """
        Create a new file with kernel-managed process and memory.
        
        :param filename: Name of the file to create
        :param content: Initial content of the file
        :param memory_required: Memory needed for the file
        :return: Process ID or None if creation failed
        """
        with self.lock:
            # Check if file already exists
            if filename in self.files:
                print(f"File {filename} already exists.")
                return None
            
            # Create process for file creation
            process = self._create_file_process(filename, content)
            
            # Attempt to create process with memory allocation
            kernel_process = self.kernel.create_process(
                process.name, 
                priority=process.priority, 
                memory_required=memory_required
            )
            
            if kernel_process:
                # Store file information
                self.files[filename] = {
                    'content': content,
                    'size': len(content),
                    'process_id': kernel_process.pid
                }
                self.save_filesystem()
                print(f"File {filename} created successfully.")
                
                return kernel_process.pid
            
            print(f"Failed to create file {filename} - process creation failed.")
            return None
    
    def list_files(self) -> list:
        """
        List all files in the file system.
        
        :return: List of filenames
        """
        
        return list(self.files.keys())
    
    def read_file(self, filename: str) -> Optional[str]:
        """
        Read content of a file.
        
        :param filename: Name of the file to read
        :return: File content or None if file doesn't exist
        """
        
        file_info = self.files.get(filename)
        return file_info['content'] if file_info else None
    
    def remove_file(self, filename: str) -> str:
        """
        Remove a file and free associated memory.
        
        :param filename: Name of the file to remove
        :return: Process ID of the removed file or error message
        """
        with self.lock:
            if filename not in self.files:
                return False
            
            # Get process ID associated with the file
            process_id = self.files[filename].get('process_id')
            
            # Remove file from filesystem
            del self.files[filename]
            
            # Free memory if process ID is available
            if process_id:
                self.kernel.memory_manager.deallocate_memory(process_id)
            
            print(f"File {filename} removed successfully.")
            self.save_filesystem()
            return process_id
        
    
    def rename_file(self, old_name: str, new_name: str) -> bool:
        """
        Rename a file.
        
        :param old_name: Current filename
        :param new_name: New filename
        :return: True if renamed successfully, False otherwise
        """
        with self.lock:
            if old_name not in self.files or new_name in self.files:
                return False
            
            # Move file info to new name
            self.files[new_name] = self.files.pop(old_name)
            self.save_filesystem()
            return True