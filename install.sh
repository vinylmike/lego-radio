#!/bin/bash

echo "🧱 LEGO Radio Installer (User-Agnostic + Clean Install)"

REPO_DIR="$HOME/lego_radio"
SYSTEMD_DIR="/etc/systemd/system"
PYTHON_PATH="/usr/bin/python3"

# Clean up any old clone
echo "🧼 Cleaning up old installation (if any)..."
rm -rf "$REPO_DIR"

# Clone latest version of the repo
echo "📥 Cloning project into $REPO_DIR..."
git clone https://github.com/vinylmike/lego-radio.git "$REPO_DIR"

# Install system dependencies
echo "🔧 Installing mpv and pip..."
sudo apt update
sudo apt install -y mpv python3-pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install --break-system-packages -r "$REPO_DIR/requirements.txt"

# Replace paths in systemd files with actual user home
echo "🔧 Configuring systemd services..."
USER_HOME=$(eval echo ~$USER)
sed "s|/home/pi|$USER_HOME|g" "$REPO_DIR/systemd/lego_radio.service" | sed "s|User=pi|User=$USER|g" | sudo tee "$SYSTEMD_DIR/lego_radio.service" > /dev/null
sed "s|/home/pi|$USER_HOME|g" "$REPO_DIR/systemd/lego_radio_web.service" | sed "s|User=pi|User=$USER|g" | sudo tee "$SYSTEMD_DIR/lego_radio_web.service" > /dev/null

# Reload and enable systemd services
echo "🔄 Enabling and starting systemd services..."
sudo systemctl daemon-reexec
sudo systemctl enable lego_radio
sudo systemctl enable lego_radio_web
sudo systemctl restart lego_radio
sudo systemctl restart lego_radio_web

# Confirm success
echo "✅ LEGO Radio is installed and running!"
echo "🌐 Access the web interface at: http://$(hostname -I | awk '{print $1}'):8080"