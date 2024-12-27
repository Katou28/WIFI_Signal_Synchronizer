import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading

def start_server_ui(host="127.0.0.1", port=65432):
    def start_server():
        nonlocal running, server_socket
        if running:
            messagebox.showwarning("Warning", "Server is already running.")
            return
        running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        thread = threading.Thread(target=server_thread, daemon=True)
        thread.start()
        log_box.insert(tk.END, f"Server started on {host}:{port}\n")

    def stop_server():
        nonlocal running, server_socket
        if not running:
            messagebox.showwarning("Warning", "Server is not running.")
            return
        running = False
        if server_socket:
            server_socket.close()
            server_socket = None
        log_box.insert(tk.END, "Server stopped.\n")

    def server_thread():
        nonlocal running, server_socket
        try:
            while running:
                try:
                    client_socket, client_address = server_socket.accept()
                    log_box.insert(tk.END, f"Connection from {client_address}\n")

                    data = client_socket.recv(1024).decode('utf-8')
                    if data:
                        try:
                            message = json.loads(data)
                            log_box.insert(tk.END, "Data received.\n")
                            if message.get("type") == "scan_result":
                                populate_table(message["data"])
                                client_socket.sendall(b"Data received successfully")
                            else:
                                log_box.insert(tk.END, "Unknown message type.\n")
                        except json.JSONDecodeError:
                            log_box.insert(tk.END, "Error decoding JSON.\n")
                    client_socket.close()
                except socket.error:
                    if running:
                        raise
        except Exception as e:
            log_box.insert(tk.END, f"Error: {e}\n")

    def populate_table(networks):
    
        "Populate the table with organized data from the client."
    
        for i in tree.get_children():
            tree.delete(i)  # Clear existing entries in the table

        for network in networks:
            ssid = network.get("SSID", "(Hidden)")
            signal = network.get("Signal", "N/A")
            tree.insert("", "end", values=(ssid, signal))

    root = tk.Tk()
    root.title("Wi-Fi Scanner Server")
    root.geometry("600x400")

    # Buttons for controlling the server
    frame = tk.Frame(root)
    frame.pack(pady=10)

    start_button = tk.Button(frame, text="Start Server", command=start_server)
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(frame, text="Stop Server", command=stop_server)
    stop_button.pack(side=tk.LEFT, padx=5)

    # Log box for server messages
    log_box = tk.Text(root, wrap=tk.WORD, height=10, width=70)
    log_box.pack(pady=10)

    # Table for organized data display
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    tree = ttk.Treeview(table_frame, columns=("SSID", "Signal"), show="headings", height=10)
    tree.heading("SSID", text="SSID")
    tree.heading("Signal", text="Signal Strength (%)")
    tree.column("SSID", width=300)
    tree.column("Signal", width=100)
    tree.pack()

    running = False
    server_socket = None

    root.mainloop()

start_server_ui()
