import psutil
import time

_last = psutil.net_io_counters()
_last_time = time.time()

def get_network_stats():
    global _last, _last_time

    current = psutil.net_io_counters()
    now = time.time()
    interval = max(now - _last_time, 1)

    stats = {
        "packets_sent": int((current.packets_sent - _last.packets_sent) / interval),
        "packets_recv": int((current.packets_recv - _last.packets_recv) / interval),
        "bytes_sent": int((current.bytes_sent - _last.bytes_sent) / interval),
        "bytes_recv": int((current.bytes_recv - _last.bytes_recv) / interval),
        "timestamp": time.strftime("%H:%M:%S")
    }

    _last = current
    _last_time = now
    return stats
