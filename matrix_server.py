import socket
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import struct
import pickle


HOST = '0.0.0.0'
PORT = 12345


def multiply_matrices(data):
    try:
        matrix_a, matrix_b = data
        result = np.dot(matrix_a, matrix_b)
        return result
    except Exception as e:
        return str(e)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Сервер запущено на {HOST}:{PORT}")

        with ThreadPoolExecutor() as executor:
            while True:
                client_socket, address = server_socket.accept()
                print(f"Підключення від: {address}")
                executor.submit(handle_client, client_socket)


def handle_client(client_socket):
    with client_socket:
        try:

            data = receive_data(client_socket)

            if not data:
                print("Порожні дані від клієнта")
                return

            matrix_a, matrix_b = data

            if matrix_a.shape[1] != matrix_b.shape[0]:
                error_message = "Неможливо перемножити: розміри матриць не відповідають вимогам."
                send_data(client_socket, error_message)
                return


            result = multiply_matrices((matrix_a, matrix_b))


            send_data(client_socket, result)

        except Exception as e:
            print(f"Помилка: {e}")
            send_data(client_socket, str(e))


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


def send_data(sock, data):
    serialized_data = pickle.dumps(data)
    data_length = len(serialized_data)
    sock.sendall(struct.pack('!I', data_length))
    sock.sendall(serialized_data)

if __name__ == "__main__":
    start_server()
