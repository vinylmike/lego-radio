#!/bin/bash

echo "🧱 LEGO Radio Installer"

REPO_DIR="/home/pi/lego_radio"
SYSTEMD_DIR="/etc/systemd/system"
PYTHON_PATH="/usr/bin/python3"

# Install system packages
echo "🔧 Installing mpv and pip..."
sudo apt update
sudo apt install -y mpv python3-pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r "$REPO_DIR/requirements.txt"

# Copy systemd service files
echo "⚙️ Installing systemd services..."
sudo cp "$REPO_DIR/systemd/lego_radio.service" "$SYSTEMD_DIR/"
sudo cp "$REPO_DIR/systemd/lego_radio_web.service" "$SYSTEMD_DIR/"

# Reload and enable services
sudo systemctl daemon-reexec
sudo systemctl enable lego_radio
sudo systemctl enable lego_radio_web
sudo systemctl start lego_radio
sudo systemctl start lego_radio_web

echo "✅ LEGO Radio is now live!"
echo "🌐 Web GUI: http://$(hostname -I | awk '{print $1}'):8080"
