#!/usr/bin/env python3
import argparse
import sys
import getpass
from pathlib import Path

# Add the parent directory to sys.path so we can import our app modules
# Assumes we are in Py_server/scripts/
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.backend.database.session import SessionLocal
from app.backend.models import User
from app.core.auth import hash_password, get_copyparty_hash
from app.core.user_sync import sync_users_to_copyparty
from app.core.logger import setup_logging

def get_db():
    return SessionLocal()

def get_password(prompt):
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    print(prompt)
    return sys.stdin.readline().strip()

def add_user(username, permissions):
    password = get_password(f"Enter password for {username}: ")
    if not password:
        print("Error: Password cannot be empty.")
        return
        
    confirm = get_password("Confirm password: ")
    
    if password != confirm:
        print("Error: Passwords do not match.")
        return

    db = get_db()
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        print(f"Error: User {username} already exists.")
        db.close()
        return

    # Generate secure hashes
    db_hash = hash_password(password)
    cp_hash = get_copyparty_hash(password)

    new_user = User(
        username=username,
        hashed_password=db_hash,
        cp_hash=cp_hash,
        permissions=permissions
    )
    
    db.add(new_user)
    try:
        db.commit()
        print(f"Successfully added user '{username}' to database.")
        sync_users_to_copyparty()
    except Exception as e:
        print(f"Error saving user: {e}")
        db.rollback()
    finally:
        db.close()

def list_users():
    db = get_db()
    users = db.query(User).all()
    print(f"\n{'ID':<4} | {'Username':<15} | {'Permissions':<12} | {'Active':<6}")
    print("-" * 45)
    for u in users:
        print(f"{u.id:<4} | {u.username:<15} | {u.permissions:<12} | {u.is_active:<6}")
    print()
    db.close()

def delete_user(username):
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"Error: User '{username}' not found.")
    else:
        db.delete(user)
        try:
            db.commit()
            print(f"User '{username}' deleted successfully.")
            sync_users_to_copyparty()
        except Exception as e:
            print(f"Error deleting user: {e}")
            db.rollback()
    db.close()

def change_password(username):
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"Error: User '{username}' not found.")
        db.close()
        return

    password = get_password(f"Enter new password for {username}: ")
    if not password:
        print("Error: Password cannot be empty.")
        db.close()
        return
        
    confirm = get_password("Confirm new password: ")
    if password != confirm:
        print("Error: Passwords do not match.")
        db.close()
        return

    user.hashed_password = hash_password(password)
    user.cp_hash = get_copyparty_hash(password)
    
    try:
        db.commit()
        print(f"Password for user '{username}' updated successfully.")
        sync_users_to_copyparty()
    except Exception as e:
        print(f"Error updating password: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Secure User Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add User
    parser_add = subparsers.add_parser("add-user", help="Add a new user")
    parser_add.add_argument("username", help="Username")
    parser_add.add_argument("--perms", default="r", help="Permissions (r, rw, rwma). Default: r")

    # List Users
    subparsers.add_parser("list-users", help="List all users")

    # Delete User
    parser_del = subparsers.add_parser("delete-user", help="Delete a user")
    parser_del.add_argument("username", help="Username")

    # Change Password
    parser_cp = subparsers.add_parser("change-password", help="Change password for a user")
    parser_cp.add_argument("username", help="Username")

    # Sync
    subparsers.add_parser("sync", help="Force sync database to Copyparty accounts file")

    args = parser.parse_args()

    # Permission Aliases
    PERM_ALIASES = {
        "ADMIN": "rwma",
        "USER": "rw",
        "GUEST": "r"
    }

    if args.command == "add-user":
        perms = PERM_ALIASES.get(args.perms.upper(), args.perms)
        add_user(args.username, perms)
    elif args.command == "list-users":
        list_users()
    elif args.command == "delete-user":
        delete_user(args.username)
    elif args.command == "change-password":
        change_password(args.username)
    elif args.command == "sync":
        sync_users_to_copyparty()
    else:
        parser.print_help()
