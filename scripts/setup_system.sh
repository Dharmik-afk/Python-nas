#!/bin/bash

# setup_system.sh - Ensures all system-level dependencies are installed (Termux optimized)

echo "--- Checking System Dependencies ---"

# Update package lists
pkg update -y

# List of required packages
PACKAGES=(
    "python"
    "git"
    "ffmpeg"
    "sqlite"
    "libjpeg-turbo"
    "build-essential"
    "python-cryptography"
    "python-pillow"
    "binutils",
    "uv"
)

# Install packages
for pkg in "${PACKAGES[@]}"; do
    echo "Ensuring $pkg is installed..."
    pkg install -y "$pkg"
done

echo "--- System Dependencies Satisfied ---"
