import json
import socket

from mini_agent.protocol import make_request

HOST = "127.0.0.1"
PORT = 8765


def send_request(request: dict) -> dict:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        client_socket.sendall(json.dumps(request).encode())

        data = client_socket.recv(4096).decode()
        return json.loads(data)


def main() -> None:
    goal = input("Enter your goal: ")

    request = make_request(
        request_id=1,
        method="run_agent",
        params={"goal": goal},
    )

    response = send_request(request)

    print(response["result"])


if __name__ == "__main__":
    main()