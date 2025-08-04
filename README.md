# 🚀 System Monitor

A sleek system monitoring tool that displays your computer's resource usage (CPU, RAM, GPU) as a **Discord Rich Presence (RPC)** status.

---

## ✨ Features
- **Real-time monitoring** of CPU, RAM, and GPU usage (supports NVIDIA, AMD, and Intel GPUs).
- **Discord RPC integration** with updates every **10 seconds**.
- **Customizable** via `config.json` (Client ID, image name from Discord Dev Portal).

---

## 📋 Requirements
- **Python 3.7 or later**
- Required libraries:
  ```bash
  pip install pypresence psutil GPUtil
  ```
- For **NVIDIA GPUs**: Ensure `nvidia-smi` is installed (comes with NVIDIA drivers).

---

## 🛠️ Installation
### 1. Clone the repository
```bash
git clone https://github.com/kmmiio99o/System-Monitor.git
cd System-Monitor
```

### 2. Install dependencies
```bash
pip install pypresence psutil GPUtil
```

### 3. Configure the tool
- Open `config.json` and provide:
  - **Client ID**: Obtain it from the [Discord Developer Portal](https://discord.com/developers/applications).
  - **Large Image Name**: The name of the image uploaded to your Discord application's Rich Presence assets.

### 4. Run the monitor
```bash
python system-monitor.py
```

---

## 🎮 Usage
- The tool will prompt you for configuration details (Client ID and image name) if not already set.
- The Discord status will update every **10 seconds** with system stats.

---

## ⚠️ Notes
- For **NVIDIA GPUs**, ensure `nvidia-smi` is accessible in your system PATH.
- The script is optimized for **minimal system impact**.
- **Image Requirements**: Upload your desired image to the Discord Developer Portal under "Rich Presence Assets" and use its exact name in the configuration.

---

## 🔧 Troubleshooting
### Discord Status Refresh Rate
- Discord **limits how often RPC statuses can update** (typically once every **15 seconds**).
  - The script is set to **10 seconds** for balance between responsiveness and stability.

### GPU Detection Issues
- If GPU stats aren't showing:
  - Ensure `nvidia-smi` is installed (for NVIDIA GPUs).
  - For AMD/Intel, install `GPUtil` and check driver compatibility.

### Image Not Displaying
- Verify that the image name in `config.json` matches the name assigned in the Discord Developer Portal.

---

## ❤️ Support
For issues or feature requests, open an issue on the [GitHub repository](https://github.com/YourUsername/In-time-something).

---

Enjoy monitoring your system in style! 🚀  
*Made with Python and a dash of magic.* ✨
