# Wi-Fi Scanner Client-Server Application

This project is a Python-based **Wi-Fi Scanner Client-Server Application** that allows a client to scan available Wi-Fi networks, display their details, and send the data to a server. The server processes the data, displays it in an organized table, and logs client connections.

---

## Features

### **Client**
- Scans available Wi-Fi networks using the `pywifi` library.
- Displays network SSIDs and signal strength as a percentage.
- Sends scanned data to the server over a TCP connection.
- Simple graphical user interface (GUI) built using `tkinter`.

### **Server**
- Accepts data from multiple clients via TCP.
- Logs incoming client connections and received data.
- Displays scanned Wi-Fi network details in a GUI table.
- Built using `tkinter` with multithreaded socket handling.

---

## Requirements

### **Dependencies**
Ensure you have the following Python libraries installed:
- `socket` (built-in)
- `json` (built-in)
- `pywifi` (for Wi-Fi scanning on the client)
- `tkinter` (for GUI on both client and server)
- `threading` (built-in)

Install `pywifi` via pip if not already installed:
```bash
pip install pywifi
