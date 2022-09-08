import os
import socket
import sys

import utils

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = utils.PORT


def client_dwd_helper(sock):
    """Helper function for DWD command"""
    received = sock.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    with open(filename, "wb") as f:
        print("Receiving file...")
        while True:
            bytes_read = sock.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
    sock.close()
    print("File downloaded successfully")
    return


if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print('\nuser@{}:{}>'.format(HOST, PORT), sep='', end='')
            msg = input(utils.colors['red'])
            print(utils.colors['reset'], end='')
            if msg == 'exit':
                print(utils.colors['green'] +
                      'Connection closed'+utils.colors['reset'])
                break
            elif msg.startswith('DWD'):
                utils.send_msg(sock, msg)
                client_dwd_helper(sock)
                print('hre in client')
                continue
            else:
                utils.send_msg(sock, msg)  # Blocks until sent
                msg = utils.recv_msg(sock)  # Block until
                print(utils.colors['green'] + msg + utils.colors['reset'])
        except ConnectionError:
            print(utils.colors['red'] + 'Socket error' + utils.colors['reset'])
            sock.close()
            break
        except KeyboardInterrupt:
            print('\nKeyboard interrupt' + utils.colors['reset'])
            sock.close()
            break
