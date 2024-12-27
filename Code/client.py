import socket
import json
from pywifi import PyWiFi, const
import tkinter as tk
from tkinter import ttk, messagebox

def dBm_to_percent(dBm):
    if dBm >= -30:
        return 100
    elif dBm <= -90:
        return 0
    else:
        return int((dBm + 90) / 60 * 100)

def scan_wifi():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    results = iface.scan_results()

    networks = {}
    for network in results:
        signal_strength = dBm_to_percent(network.signal)
        if network.ssid not in networks or signal_strength > networks[network.ssid]:
            networks[network.ssid] = signal_strength

    return [{"SSID": ssid, "Signal": signal} for ssid, signal in networks.items()]

def send_data_to_server(data, host="127.0.0.1", port=65432):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        message = json.dumps({"type": "scan_result", "data": data})
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return response
    except Exception as e:
        return f"Error: {e}"

def create_client_ui():
    def scan_and_display():
        networks = scan_wifi()
        if networks:
            tree.delete(*tree.get_children())
            for network in networks:
                tree.insert("", "end", values=(network["SSID"], network["Signal"]))
        else:
            messagebox.showinfo("Scan Result", "No Wi-Fi networks found.")

    def send_data():
        networks = scan_wifi()
        if networks:
            response = send_data_to_server(networks)
            messagebox.showinfo("Server Response", response)
        else:
            messagebox.showwarning("Warning", "No Wi-Fi data to send.")

    root = tk.Tk()
    root.title("Wi-Fi Scanner Client")
    root.geometry("400x300")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    scan_button = tk.Button(frame, text="Scan Wi-Fi", command=scan_and_display)
    scan_button.pack(side=tk.LEFT, padx=5)

    send_button = tk.Button(frame, text="Send Data to Server", command=send_data)
    send_button.pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(root, columns=("SSID", "Signal"), show="headings", height=10)
    tree.heading("SSID", text="SSID")
    tree.heading("Signal", text="Signal Strength (%)")
    tree.pack(pady=10)

    root.mainloop()


create_client_ui()
