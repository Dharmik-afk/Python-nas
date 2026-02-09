import socket
import logging
import os
import stat

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

def get_public_url(port: int, host: str = "0.0.0.0") -> str:
    """
    Determines the best URL to reach the server.
    Priority:
    1. PUBLIC_URL environment variable.
    2. LAN IP (if host is 0.0.0.0).
    3. Host:Port.
    """
    public_url = os.environ.get("PUBLIC_URL")
    if public_url:
        return public_url.rstrip("/")

    if host == "0.0.0.0":
        host = get_lan_ip()
    
    return f"http://{host}:{port}"

def generate_opener_script(port: int, host: str = "0.0.0.0", output_file: str = "open_server.sh"):
    """
    Generates a shell script to open the server URL in the Android browser.
    """
    url = get_public_url(port, host)
    
    content = (
        "#!/bin/bash\n"
        f"am start -a android.intent.action.VIEW -d \"{url}\" > /dev/null 2>&1 &\n"
    )
    
    try:
        with open(output_file, "w") as f:
            f.write(content)
        
        # Make executable: rwxr-xr-x
        os.chmod(output_file, 0o755)
        logger.info(f"Generated opener script: {output_file} -> {url}")
    except Exception as e:
        logger.error(f"Failed to generate opener script: {e}")
