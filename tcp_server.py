import socket
import threading

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Non-privileged port

def handle_client(conn, addr):
    """Handle communication with a single client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024)  # Receive up to 1024 bytes
            if not data:
                print(f"[DISCONNECT] {addr} disconnected.")
                break  # Client closed connection

            message = data.decode('utf-8').strip()
            print(f"[RECEIVED] From {addr}: {message}")

            # Prepare and send reply
            reply = f"Server received: {message}"
            conn.sendall(reply.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()

def start_server():
    """Start the TCP server and keep it running."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            # Handle each client in a separate thread
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()