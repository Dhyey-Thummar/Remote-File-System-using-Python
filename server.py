import socket

import utils

HOST = ''
PORT = 4040


def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.settimeout(5)
    sock.listen(100)
    return sock


def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    try:
        while True:
            msg = utils.recv_msg(sock)  # Blocks until received
            # complete message
            msg = msg.lower()
            print('Received message: ' + msg)
            if(msg == "cwd"):
                utils.CWD(sock)
            elif(msg == "ls"):
                utils.LS(sock)
            elif(msg.startswith("cd")):
                utils.CD(sock, msg)
            elif(msg.startswith("dwd")):
                utils.DWD(sock, msg)
                sock.close()
                break
            elif(msg.startswith("upd")):
                utils.UPD(sock)
                sock.close()
                break
            elif(msg == "exit"):
                print("Closing connection")
                sock.close()
                break
            else:
                utils.send_msg(sock, "Invalid command")
                continue
    except (ConnectionError, BrokenPipeError) as err:
        print(err)


if __name__ == '__main__':
    listen_sock = create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))
    try:
        while True:
            try:
                client_sock, addr = listen_sock.accept()
                print('Connection from {}'.format(addr))
                handle_client(client_sock, addr)
            except socket.timeout:
                print('Timed out, listening again')
    except KeyboardInterrupt:
        print('Keyboard interrupt, killing server')
    listen_sock.close()
