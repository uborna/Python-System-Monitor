import psutil,os,platform,time
class SystemMonitor:
    def __init__(self,interval=1):
        self._interval = interval
        self._user_system = platform.uname()
    def get_processor(self):
        processor = platform.processor()

        if not processor:
            processor = platform.machine()

        return processor
    def user_system(self):
        sysdict = {"OS":self._user_system.system,
                   "OS_Type":self._user_system.node,
                   "Processor": self.get_processor()
                   }
        return sysdict
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


s = SystemMonitor()
print(s.user_system())