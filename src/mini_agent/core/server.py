import json
import socket

from mini_agent.agent.runner import run_agent
from mini_agent.protocol import make_response

HOST = "127.0.0.1"
PORT = 8765


def handle_request(request: dict) -> dict:
    method = request["method"]

    if method == "ping":
        return make_response(
            request_id=request["id"],
            result="pong",
        )

    if method == "run_agent":
        goal = request["params"]["goal"]

        result = run_agent(goal)

        return make_response(
            request_id=request["id"],
            result=result,
        )

    return make_response(
        request_id=request["id"],
        result=f"Unknown method: {method}",
    )


def run_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Core daemon listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()

            with conn:
                print(f"Connected by {addr}")

                data = conn.recv(4096).decode()
                request = json.loads(data)

                response = handle_request(request)

                conn.sendall(json.dumps(response).encode())


if __name__ == "__main__":
    run_server()