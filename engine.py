import psutil
class SystemMonitor:
    def __init__(self,interval):
        self._interval = interval
    
    def get_cpu_usage(self):
        cpu_usage = psutil.cpu_percent(interval=self._interval)
        return f"{cpu_usage:.1f}"
    def get_memory_usage_percentage(self):
        memory_usage = psutil.virtual_memory().percent
        return f"{memory_usage:.1f}"
    
    def get_memory_used(self):
        ram_ued_bytes = psutil.virtual_memory().used
        memory_usage = ram_ued_bytes / (1024**3)
        return f"{memory_usage:.2f}"