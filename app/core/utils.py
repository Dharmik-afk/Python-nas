import socket
import logging

logger = logging.getLogger(__name__)

def get_lan_ip() -> str:
    """
    Attempts to determine the device's local network IP address.

    Returns:
        The LAN IP address as a string, or '127.0.0.1' if it cannot be determined.
    """
    try:
        # Create a dummy socket to connect to a public DNS server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # The connect call doesn't actually send data
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            logger.debug(f"Successfully determined LAN IP: {ip_address}")
            return ip_address
    except Exception as e:
        logger.warning(
            f"Could not determine LAN IP address. "
            f"Falling back to 127.0.0.1. Error: {e}"
        )
        return "127.0.0.1"
