import socket

HOST = '127.0.0.1'  # Server address
PORT = 65432        # Server port

def run_client():
    """Connect to the server and send messages."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            print("[CONNECTED] to server.")

            while True:
                msg = input("Enter message (or 'quit' to exit): ").strip()
                if msg.lower() == 'quit':
                    print("[EXIT] Closing connection.")
                    break

                client.sendall(msg.encode('utf-8'))
                data = client.recv(1024)
                print(f"[SERVER REPLY] {data.decode('utf-8')}")
    except ConnectionRefusedError:
        print("[ERROR] Server is not running.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    run_client()