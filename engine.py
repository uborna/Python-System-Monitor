import psutil,os,platform,time
class SystemMonitor:
    def __init__(self,interval=1):
        self._interval = interval
        self._user_system = platform.uname()
        self._old_net = psutil.net_io_counters()
        self._old_time = time.monotonic()
        
    def get_processor(self):
        return platform.processor() or platform.machine()
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
    def get_disk_usage(self):
            return psutil.disk_usage("/").percent
    
    def get_disk_used(self):
        return round(psutil.disk_usage("/").used / (1024 ** 3), 1)
    
    def get_network_speed(self):
        net = psutil.net_io_counters()
        now = time.monotonic()
        elapsed = max(now - self._old_time, 0.001)
        speed = ((net.bytes_recv - self._old_net.bytes_recv) + (net.bytes_sent - self._old_net.bytes_sent)) / 1024 / elapsed
        self._old_net = net
        self._old_time = now
        return round(speed, 1)
    
    def get_battery(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return None, "No battery"
        return battery.percent, "Charging" if battery.power_plugged else "On battery"
    

# s = SystemMonitor()
# print(s.user_system())