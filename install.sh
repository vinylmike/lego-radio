#!/bin/bash

echo "🧱 LEGO Radio Installer (User-Agnostic)"

REPO_DIR="$HOME/lego_radio"
SYSTEMD_DIR="/etc/systemd/system"

# Clean previous clone
echo "🧼 Cleaning up old install..."
rm -rf "$REPO_DIR"

# Clone fresh
echo "📥 Cloning latest repo..."
git clone https://github.com/vinylmike/lego-radio.git "$REPO_DIR"

# Install system dependencies
echo "🔧 Installing mpv and pip..."
sudo apt update
sudo apt install -y mpv python3-pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install --break-system-packages -r "$REPO_DIR/requirements.txt"

# Install systemd services dynamically
echo "🔧 Setting up systemd services..."
USER_HOME=$(eval echo ~$USER)

sed "s|REPLACEME_HOME|$USER_HOME|g; s|REPLACEME_USER|$USER|g" "$REPO_DIR/systemd/lego_radio.service" | sudo tee "$SYSTEMD_DIR/lego_radio.service" > /dev/null
sed "s|REPLACEME_HOME|$USER_HOME|g; s|REPLACEME_USER|$USER|g" "$REPO_DIR/systemd/lego_radio_web.service" | sudo tee "$SYSTEMD_DIR/lego_radio_web.service" > /dev/null

# Reload and start
sudo systemctl daemon-reexec
sudo systemctl enable lego_radio
sudo systemctl enable lego_radio_web
sudo systemctl restart lego_radio
sudo systemctl restart lego_radio_web

echo "✅ LEGO Radio is live!"
echo "🌐 Visit http://$(hostname -I | awk '{print $1}'):8080"
