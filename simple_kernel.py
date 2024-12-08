import heapq
import threading
import time
import uuid
from typing import Dict, List, Callable, Any, Optional
import random

class MemoryManager:
    def __init__(self, total_memory: int = 1024):
        """
        Simulate memory management with basic allocation and deallocation.
        
        :param total_memory: Total available memory in bytes
        """
        self.total_memory = total_memory
        self.used_memory = 0
        self.memory_map: Dict[str, int] = {}  # Process ID to memory allocation
    
    def allocate_memory(self, process_id: str, size: int) -> bool:
        """
        Allocate memory for a process.
        
        :param process_id: Unique identifier for the process
        :param size: Memory size to allocate
        :return: True if allocation successful, False otherwise
        """
        if self.used_memory + size > self.total_memory:
            return False
        
        self.memory_map[process_id] = size
        self.used_memory += size
        return True
    
    def deallocate_memory(self, process_id: str):
        """
        Free memory allocated to a process.
        
        :param process_id: Unique identifier for the process
        """
        if process_id in self.memory_map:
            self.used_memory -= self.memory_map[process_id]
            del self.memory_map[process_id]
    
    def get_free_memory(self) -> int:
        """
        Get available memory.
        
        :return: Free memory in bytes
        """
        return self.total_memory - self.used_memory

class InterruptController:
    def __init__(self):
        """
        Simulate an interrupt controller with priority-based handling.
        """
        self.interrupt_queue: List[tuple] = []
        self.interrupt_lock = threading.Lock()
    
    def raise_interrupt(self, priority: int, handler: Callable):
        """
        Raise an interrupt with a specific priority.
        
        :param priority: Interrupt priority (lower number = higher priority)
        :param handler: Function to handle the interrupt
        """
        with self.interrupt_lock:
            heapq.heappush(self.interrupt_queue, (priority, handler))
    
    def handle_interrupts(self):
        """
        Process interrupts in order of priority.
        """
        with self.interrupt_lock:
            while self.interrupt_queue:
                _, handler = heapq.heappop(self.interrupt_queue)
                try:
                    handler()
                except Exception as e:
                    print(f"Interrupt handler error: {e}")

class Process:
    def __init__(self, name: str, priority: int = 0):
        """
        Represent a process in the system.
        
        :param name: Process name
        :param priority: Process priority
        """
        self.pid = str(uuid.uuid4())
        self.name = name
        self.priority = priority
        self.state = 'NEW'
        self.context = {}  # Simulated process context
    
    def __lt__(self, other):
        """
        Allow comparison for priority-based scheduling.
        
        :param other: Another process to compare
        :return: Comparison result based on priority
        """
        return self.priority < other.priority

class ProcessScheduler:
    def __init__(self):
        """
        Simulate a simple process scheduler using priority queue.
        """
        self.ready_queue: List[Process] = []
        self.running_process: Optional[Process] = None
        self.scheduler_lock = threading.Lock()
    
    def add_process(self, process: Process):
        """
        Add a process to the ready queue.
        
        :param process: Process to add
        """
        with self.scheduler_lock:
            heapq.heappush(self.ready_queue, process)
            process.state = 'READY'
        return process
    
    def schedule_next_process(self):
        """
        Schedule the next process to run.
        """
        with self.scheduler_lock:
            if self.ready_queue:
                # Select highest priority process
                self.running_process = heapq.heappop(self.ready_queue)
                self.running_process.state = 'RUNNING'
                print(f"Running process: {self.running_process.name} (PID: {self.running_process.pid})")
            else:
                self.running_process = None
        return self.running_process
    
    def terminate_current_process(self):
        """
        Terminate the currently running process.
        """
        if self.running_process:
            self.running_process.state = 'TERMINATED'
            print(f"Terminated process: {self.running_process.name}")
            self.running_process = None
        return self.running_process

class Kernel:
    def __init__(self):
        """
        Main kernel class integrating memory management, 
        process scheduling, and interrupt handling.
        """
        self.memory_manager = MemoryManager()
        self.interrupt_controller = InterruptController()
        self.process_scheduler = ProcessScheduler()
        
        # Kernel threads
        self.scheduler_thread = None
        self.interrupt_thread = None
        self.running = False
    
    def start(self):
        """
        Start kernel services.
        """
        self.running = True
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        # Start interrupt handling thread
        self.interrupt_thread = threading.Thread(target=self._interrupt_loop)
        self.interrupt_thread.daemon = True
        self.interrupt_thread.start()
    
    def stop(self):
        """
        Stop kernel services.
        """
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        if self.interrupt_thread:
            self.interrupt_thread.join()
    
    def create_process(self, name: str, priority: int = 0, memory_required: int = 100) -> Optional[Process]:
        """
        Create and add a new process.
        
        :param name: Process name
        :param priority: Process priority
        :param memory_required: Memory needed for the process
        :return: Created process or None if creation fails
        """
        process = Process(name, priority)
        
        # Attempt to allocate memory
        if self.memory_manager.allocate_memory(process.pid, memory_required):
            self.process_scheduler.add_process(process)
            return process
        
        print(f"Failed to create process {name}: Insufficient memory")
        return None
    
    def _scheduler_loop(self):
        """
        Kernel scheduling loop.
        """
        while self.running:
            self.process_scheduler.schedule_next_process()
            time.sleep(1)  # Simulate time slice

            self.process_scheduler.terminate_current_process()
                
            # Free associated memory
            if self.process_scheduler.running_process:
                self.memory_manager.deallocate_memory(
                    self.process_scheduler.running_process.pid
                )

    def _interrupt_loop(self):
        """
        Kernel interrupt handling loop.
        """
        while self.running:
            # # Simulate occasional random interrupts
            # if random.random() < 0.2:
            #     self._generate_random_interrupt()
            
            self.interrupt_controller.handle_interrupts()
            time.sleep(0.5)
    
    def _generate_random_interrupt(self):
        """
        Generate a random interrupt for demonstration.
        """
        def sample_interrupt():
            print(f"Handling simulated interrupt - Current free memory: {self.memory_manager.get_free_memory()} bytes")
        
        # Generate interrupt with random priority
        self.interrupt_controller.raise_interrupt(
            random.randint(1, 10),  # Priority
            sample_interrupt
        )