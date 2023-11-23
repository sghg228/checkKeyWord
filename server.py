import socket
import json

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Сервер слушает на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Получено соединение от {addr}")

        with client_socket:
            data = receive_data(client_socket)
            print(f"Полученные данные: ")
            print([str(x) + ' ' for x in data])
            #send_response(client_socket, "Данные успешно получены")

def receive_data(client_socket):
    data = b""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        data += chunk

    return json.loads(data.decode('utf-8'))

def send_response(client_socket, response):
    client_socket.send(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()
