import socket

def get_local_ip():
    """
    Returns the local IP address of the current system
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception:
        return "Unable to detect IP"
