import socket
import sys
import encryption as crypt  # Path: encryption.py
import utils  # Path: utils.py

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = utils.PORT


if __name__ == '__main__':
    # eType = input(
    #     "Encryption type available:\n1. Substitute\n2. Transpose\n3. None\nEnter encryption type: ")
    # if eType == "1":
    #     crypt.encrypt_type = "substitute"
    #     crypt.offset = int(input("Enter offset: "))
    # elif eType == "2":
    #     crypt.encrypt_type = "transpose"
    # elif eType == "3":
    #     crypt.encrypt_type = "plain"

    while True:
        try:
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            # utils.send_msg(sock, f"{crypt.encrypt_type}{SEPARATOR}{crypt.offset}")
            print('\nuser@{}:{}>'.format(HOST, PORT), sep='', end='')
            msg = input(utils.colors['red'])
            msg = msg.lower()
            print(utils.colors['reset'], end='')
            if msg == 'exit':
                print(utils.colors['green'] +
                      'Connection closed'+utils.colors['reset'])
                break
            elif msg.startswith('dwd'):
                utils.send_msg(sock, msg)
                utils.client_dwd_helper(sock)
                continue
            elif msg.startswith('upd'):
                utils.send_msg(sock, msg)
                utils.client_upd_helper(sock, msg)
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
