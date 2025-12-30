import requests
import sys
import os
import time
import subprocess
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "restricted"
PASSWORD = "restricted"
TEST_FILE = "reproduce_test.txt"

def run_command(command):
    """Runs a shell command."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result

def setup_user():
    """Ensures the restricted user exists."""
    print(f"[*] Checking for user '{USERNAME}'...")
    # List users to check existence
    res = run_command("python3 scripts/manage.py list-users")
    if USERNAME in res.stdout:
        print(f"    User '{USERNAME}' already exists.")
        return

    print(f"[*] Creating user '{USERNAME}' with 'r' permissions...")
    # Create user non-interactively
    cmd = f"printf '{PASSWORD}\n{PASSWORD}\n' | python3 scripts/manage.py add-user {USERNAME} --perms r"
    res = run_command(cmd)
    if res.returncode != 0:
        print(f"[!] Failed to create user: {res.stderr}")
        sys.exit(1)
    print("    User created successfully.")

def setup_file():
    """Creates a dummy file for deletion testing."""
    file_path = Path("storage/files") / TEST_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        print(f"[*] Creating test file '{TEST_FILE}'...")
        file_path.write_text("This is a test file for permission verification.")
    else:
        print(f"[*] Test file '{TEST_FILE}' already exists.")

def test_deletion():
    """Attempts to delete the file as the restricted user."""
    print(f"[*] Attempting to login as '{USERNAME}'...")
    session = requests.Session()
    
    # 1. Login
    login_url = f"{BASE_URL}/api/v1/auth/login"
    try:
        r = session.post(login_url, data={"username": USERNAME, "password": PASSWORD})
    except requests.exceptions.ConnectionError:
        print(f"[!] Could not connect to {BASE_URL}. Is the server running?")
        sys.exit(1)

    if r.status_code != 200:
        print(f"[!] Login failed: {r.status_code} - {r.text}")
        sys.exit(1)
    print("    Login successful.")

    # 2. Delete
    delete_url = f"{BASE_URL}/api/v1/fs/{TEST_FILE}"
    print(f"[*] Attempting DELETE request to: {delete_url}")
    r = session.delete(delete_url)
    
    print(f"[*] DELETE Response Code: {r.status_code}")
    
    if r.status_code == 403:
        print("\n[SUCCESS] Permission Denied (403). The restricted user CANNOT delete files.")
        print("          The fix is verified.")
    elif r.status_code == 200 or r.status_code == 204:
        print("\n[FAILURE] Deletion Succeeded! The restricted user WAS ABLE to delete the file.")
        print("          The issue is reproduced.")
    else:
        print(f"\n[?] Unexpected response: {r.status_code}")
        print(f"    Body: {r.text}")

if __name__ == "__main__":
    print("=== Permission Verification Script ===")
    
    # Ensure we are in project root
    if not Path("scripts/manage.py").exists():
        print("[!] Please run this script from the project root directory.")
        sys.exit(1)

    setup_user()
    setup_file()
    
    # Check if server is likely running by simple connect
    try:
        requests.get(f"{BASE_URL}/health", timeout=1)
    except requests.exceptions.ConnectionError:
        print("\n[!] Server does not appear to be running on port 8000.")
        print("    Please start the server in a separate terminal using: make run")
        sys.exit(1)
        
    test_deletion()
