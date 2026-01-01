# Custom Device Configuration

This guide explains how to add custom device types with personalized icons and labels to the Ultimate Kea Dashboard.

## Configuration File

**Location**: `etc/custom-devices.json`

The configuration file allows you to define custom devices that will be recognized by the dashboard with specific icons and labels.

## File Structure

```json
{
  "custom_devices": [
    {
      "hostname": "device-name",
      "type": "device-type",
      "emoji": "🎮",
      "label": "Custom Label",
      "description": "Device description",
      "icon_theme": "theme-name"
    }
  ],
  "device_types": {
    "device-type": {
      "emoji": "🎮",
      "default_label": "Default Label"
    }
  }
}
```

## Parameters

### Custom Devices

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hostname` | string | ✅ | Device hostname (partial match) |
| `type` | string | ✅ | Device type identifier |
| `emoji` | string | ✅ | Emoji icon (fallback if no SVG) |
| `label` | string | ✅ | Display label in dashboard |
| `description` | string | ❌ | Human-readable description |
| `icon_theme` | string | ❌ | SVG icon theme variant |

### Device Types

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `emoji` | string | ✅ | Default emoji for type |
| `default_label` | string | ✅ | Default label for type |

## Examples

### Gaming PCs

```json
{
  "custom_devices": [
    {
      "hostname": "marvin",
      "type": "gaming-pc",
      "emoji": "🎮",
      "label": "Gaming PC Maître",
      "description": "PC Gaming puissant avec setup RGB et écran large",
      "icon_theme": "master"
    },
    {
      "hostname": "shepard",
      "type": "gaming-pc",
      "emoji": "🎮",
      "label": "Gaming PC Apprenti",
      "description": "Mini PC gaming compact",
      "icon_theme": "apprentice"
    }
  ],
  "device_types": {
    "gaming-pc": {
      "emoji": "🎮",
      "default_label": "Gaming PC"
    }
  }
}
```

### Home Server

```json
{
  "custom_devices": [
    {
      "hostname": "homelab",
      "type": "server",
      "emoji": "🖥️",
      "label": "Home Server",
      "description": "Proxmox hypervisor",
      "icon_theme": "proxmox"
    }
  ]
}
```

### Smart Home Devices

```json
{
  "custom_devices": [
    {
      "hostname": "living-room-tv",
      "type": "smart-tv",
      "emoji": "📺",
      "label": "Living Room TV",
      "icon_theme": "samsung"
    },
    {
      "hostname": "kitchen-alexa",
      "type": "smart-speaker",
      "emoji": "🔊",
      "label": "Kitchen Echo",
      "icon_theme": "alexa"
    }
  ]
}
```

## Icon Themes

### Built-in Gaming PC Themes

The dashboard includes custom SVG icons for gaming PCs:

- **`master`**: High-end gaming setup with large curved monitor and RGB
- **`apprentice`**: Compact mini PC with small monitor
- **`generic`**: Standard gaming PC with tower case

### Adding Custom Icons

Custom SVG icons can be added by modifying `lib/custom_devices.py` and adding a new theme in the `generate_gaming_pc_svg()` function.

## Hostname Matching

The `hostname` field supports **partial matching** (case-insensitive):

- `"marvin"` matches: `marvin`, `marvin-pc`, `MARVIN.local`
- `"office"` matches: `office-pc`, `my-office`, `office-laptop`

## Priority

Custom devices are checked **FIRST** before generic pattern matching, ensuring your specific devices are always correctly identified.

## Reload Configuration

After modifying `etc/custom-devices.json`, restart the dashboard:

```bash
sudo systemctl restart ultimate-dashboard
```

## Validation

Test your configuration:

```bash
# Check JSON syntax
python3 -m json.tool etc/custom-devices.json

# View loaded devices in logs
journalctl -u ultimate-dashboard -n 50 | grep "custom devices"
```

## Default Configuration

The default configuration includes examples for two gaming PCs. You can modify, extend, or replace these with your own devices.

## Supported Device Types

While you can create any custom type, these are commonly used:

- `gaming-pc` - Gaming computers
- `server` - Servers and NAS
- `smart-tv` - Smart TVs
- `smart-speaker` - Voice assistants
- `camera` - Security cameras
- `iot` - IoT devices
- `network` - Network equipment

## Troubleshooting

### Device not detected

1. Check hostname spelling in config
2. Verify JSON syntax
3. Check dashboard logs for errors
4. Restart dashboard service

### Icon not showing

1. Verify `icon_theme` exists
2. Check SVG generation in `lib/custom_devices.py`
3. Clear browser cache

### Configuration not loading

1. Check file permissions: `chmod 644 etc/custom-devices.json`
2. Verify JSON syntax: `python3 -m json.tool etc/custom-devices.json`
3. Check dashboard logs: `journalctl -u ultimate-dashboard -n 100`

## Contributing

Feel free to contribute new icon themes or device types to the project!

---

**Related Files**:
- `etc/custom-devices.json` - Configuration file
- `lib/custom_devices.py` - Module implementation
- `lib/device_detection.py` - Device detection logic
