import socket
import datetime
import logging
import json
from datetime import datetime

# Logging setup
logger = logging.getLogger("honeypot_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("../logs/attacks.log")
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

# Function to log attacks
def log_event(ip, port, command, status):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source_ip": ip,
        "port": port,
        "command": command,
        "status": status
    }
    logger.info(json.dumps(entry))

HOST = '0.0.0.0'
PORT = 2323

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("🚨 Fake Telnet device running on port 2323...")

while True:
    client_socket, client_address = server.accept()
    print(f"[+] Connection from {client_address[0]}")

    # Log connection
    with open("honeypot_logs.txt", "a") as log_file:
        log_file.write(f"\n--- New Connection ---\n")
        log_file.write(f"Time: {datetime.now()}\n")
        log_file.write(f"IP: {client_address[0]}\n")

    client_socket.sendall(b"Welcome to SmartPlug 1.0\r\nLogin: ")

    while True:
        try:
            buffer = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                buffer += chunk
                if b"\n" in chunk or b"\r" in chunk:
                    break

            command = buffer.decode().strip()

            if command == "help":
                client_socket.sendall(
                    b"Available commands: help, status, reboot, exit, ls, cat, ping, version\r\n> "
                )
            elif command == "status":
                client_socket.sendall(
                    b"Device status: ONLINE, Power: ON, Temperature: 36C\r\n> "
                )
            elif command == "reboot":
                client_socket.sendall(b"Rebooting device...\r\n> ")
            elif command == "exit":
                client_socket.sendall(b"Logging out...\r\n")
                client_socket.close()
                break
            elif command == "ls":
                client_socket.sendall(b"config.txt  logs/  firmware.bin\r\n> ")
            elif command == "cat config.txt":
                client_socket.sendall(
                    b"username=admin\npassword=admin123\nwifi_ssid=SmartPlugNet\nwifi_pass=12345678\r\n> "
                    )
            elif command == "ping":
                client_socket.sendall(
                    b"Pinging 8.8.8.8 with 32 bytes of data...\nReply from 8.8.8.8: bytes=32 time=20ms TTL=54\r\n> "
                )
            elif command == "version":
                client_socket.sendall(b"SmartPlug Firmware v1.2.7 - Build 0425\r\n> ")
            else:
                client_socket.sendall(b"Command not recognized\r\n> ")

            buffer = b""

            # Log the command attempt
            log_event(client_address[0], PORT, command, "command received")

            with open("honeypot_logs.txt", "a") as log_file:
                log_file.write(f"{client_address[0]} > {command}\n")

            #client_socket.sendall(b"Command not recognized\r\n> ")
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break