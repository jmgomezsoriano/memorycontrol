from memorycontrol import monitor

command_line = "uvicorn api.server:app --port 8001"

memory_limit = 100  
kill_memory_threshold = 200  
check_interval = 5  

monitor(command_line, memory_limit, kill_memory_threshold, check_interval)
