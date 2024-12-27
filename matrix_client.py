import socket
import numpy as np
import struct
import pickle


HOST = '127.0.0.1'
PORT = 12345

def generate_matrices():
    N, M, L = np.random.randint(1001, 1101, size=3)
    matrix_a = np.random.randint(0, 100, size=(N, M))
    matrix_b = np.random.randint(0, 100, size=(M, L))
    return matrix_a, matrix_b


def send_data(sock, data):
    serialized_data = pickle.dumps(data)
    data_length = len(serialized_data)
    sock.sendall(struct.pack('!I', data_length))
    sock.sendall(serialized_data)

def receive_data(sock):
    data_length_bytes = sock.recv(4)
    if not data_length_bytes:
        return None

    data_length = struct.unpack('!I', data_length_bytes)[0]
    data = b''
    while len(data) < data_length:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet

    return pickle.loads(data)


def start_client():
    matrix_a, matrix_b = generate_matrices()
    print(f"Згенеровано матриці:")
    print(f"Матриця A (розмір {matrix_a.shape}):\n{matrix_a}")
    print(f"Матриця B (розмір {matrix_b.shape}):\n{matrix_b}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))


        send_data(client_socket, (matrix_a, matrix_b))


        result = receive_data(client_socket)

        if isinstance(result, str):
            print(f"Помилка від сервера: {result}")
        else:
            print(f"Результат множення (розмір {result.shape}):\n{result}")

if __name__ == "__main__":
    start_client()
