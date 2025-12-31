#!/bin/bash
# Quick script to push to GitHub

echo "=========================================="
echo "Ultimate Kea Dashboard - GitHub Push"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [[ ! -f "install.sh" ]]; then
    echo "Error: Run this script from the repository root"
    exit 1
fi

# Initialize git if not already done
if [[ ! -d ".git" ]]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial release v1.0.0 - Ultimate Kea DHCP Dashboard

Features:
- Real-time DHCP lease monitoring
- Network device scanning (DHCP pool and static devices)
- System metrics visualization (CPU, RAM, Network, Disk)
- Multi-theme support (Blossom, Sunset, Ocean, Forest, Night)
- Individual and global scan control
- Service detection and device type identification
- Modern, responsive UI with auto-refresh
- SSL/TLS support
- Interactive installer with professional interface"
    echo "✓ Repository initialized and committed"
else
    echo "✓ Git repository already initialized"
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "✓ Remote 'origin' already configured"
else
    echo ""
    echo "Adding remote origin..."
    git remote add origin git@github.com:NeySlim/ultimate-kea-dashboard.git
    echo "✓ Remote added"
fi

echo ""
echo "Testing SSH connection to GitHub..."
ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" && echo "✓ SSH authentication successful" || echo "⚠ SSH may need configuration"

echo ""
read -p "Ready to push to GitHub? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    echo ""
    echo "Creating and pushing tag v1.0.0..."
    git tag -a v1.0.0 -m "Release v1.0.0 - Initial public release" 2>/dev/null || echo "Tag already exists"
    git push origin v1.0.0 2>/dev/null || git push origin v1.0.0 --force
    
    echo ""
    echo "=========================================="
    echo "✓ Successfully pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Go to: https://github.com/NeySlim/ultimate-kea-dashboard"
    echo "2. Create a release from tag v1.0.0"
    echo "3. See SETUP_REPO.md for detailed instructions"
    echo ""
else
    echo "Push cancelled."
fi
