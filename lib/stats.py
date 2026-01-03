"""System statistics collection"""
import psutil
import time


_last_net = {'bytes_sent': 0, 'bytes_recv': 0, 'time': time.time()}
_last_cpu = {'values': [0], 'time': 0}
_stats_cache = {'data': None, 'time': 0}
CACHE_TTL = 0.5  # Cache stats for 500ms to avoid constant CPU checks


def get_system_stats():
    """Get real-time system statistics with caching"""
    global _last_net, _last_cpu, _stats_cache
    
    current_time = time.time()
    
    # Return cached stats if fresh enough
    if _stats_cache['data'] and (current_time - _stats_cache['time']) < CACHE_TTL:
        return _stats_cache['data']
    
    try:
        # CPU usage per core (use interval=0 for instant, no blocking)
        cpu_percent = psutil.cpu_percent(interval=0, percpu=True)
        
        # If all zeros (first call), use last known values
        if sum(cpu_percent) == 0 and _last_cpu['values']:
            cpu_percent = _last_cpu['values']
        else:
            _last_cpu = {'values': cpu_percent, 'time': current_time}
        
        # RAM usage (GB)
        mem = psutil.virtual_memory()
        ram_used_gb = mem.used / (1024**3)
        ram_total_gb = mem.total / (1024**3)
        ram_percent = (ram_used_gb / ram_total_gb) * 100  # Calculate from GB values
        
        # Network I/O (Mbps - megabits per second)
        net = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - _last_net['time']
        
        if time_delta > 0:
            bytes_sent_delta = net.bytes_sent - _last_net['bytes_sent']
            bytes_recv_delta = net.bytes_recv - _last_net['bytes_recv']
            
            # Convert to Mbps (megabits per second)
            net_sent_mbps = (bytes_sent_delta * 8) / (time_delta * 1000000)
            net_recv_mbps = (bytes_recv_delta * 8) / (time_delta * 1000000)
        else:
            net_sent_mbps = 0
            net_recv_mbps = 0
        
        _last_net = {
            'bytes_sent': net.bytes_sent,
            'bytes_recv': net.bytes_recv,
            'time': current_time
        }
        
        # Disk usage (GB)
        disk = psutil.disk_usage('/')
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        disk_percent = (disk_used_gb / disk_total_gb) * 100  # Calculate from GB values
        
        stats_data = {
            "cpu_cores": [round(c, 1) for c in cpu_percent],
            "cpu_avg": round(sum(cpu_percent) / len(cpu_percent), 1),
            "ram": round(ram_percent, 1),
            "ram_used_gb": round(ram_used_gb, 1),
            "ram_total_gb": round(ram_total_gb, 1),
            "net_sent": round(net_sent_mbps, 2),
            "net_recv": round(net_recv_mbps, 2),
            "disk": round(disk_percent, 1),
            "disk_used_gb": round(disk_used_gb, 1),
            "disk_total_gb": round(disk_total_gb, 1)
        }
        
        # Cache the result
        _stats_cache = {'data': stats_data, 'time': current_time}
        
        return stats_data
    except Exception as e:
        print(f"[ERROR] Failed to get system stats: {e}")
        import traceback
        traceback.print_exc()
        return {
            "cpu_cores": [0],
            "cpu_avg": 0,
            "ram": 0,
            "ram_used_gb": 0,
            "ram_total_gb": 0,
            "net_sent": 0,
            "net_recv": 0,
            "disk": 0,
            "disk_used_gb": 0,
            "disk_total_gb": 0
        }
