# This is the client side of the file service program


import socket  # Import socket module
import sys  # for sys.argv
import encryption as crypt  # Path: encryption.py
import utils  # Path: utils.py

SEPARATOR = "<SEPARATOR>"  # Used to separate file name and file size
BUFFER_SIZE = 4096  # 4KB of buffer size for each file chunk
# Default host is localhost
HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = utils.PORT  # Default port is 4040


# Here we have used __name__ == '__main__' to make sure that the code is only executed
# when the script is run directly by the interpreter and not used as an imported module.
if __name__ == '__main__':
    # Below commented code is for testing purposes. I tried to create a prompt to take in encryption type and offset, but it didn't work.
    # The problem was that I was unable to synchronize the value of ENCRYPT_TYPE and OFFSET with the values in encryption.py.
    # I tried to use globals() and locals() but it didn't work.

    # eType = input(
    #     "Encryption type available:\n1. Substitute\n2. Transpose\n3. None\nEnter encryption type: ")
    # if eType == "1":
    #     crypt.encrypt_type = "substitute"
    #     crypt.offset = int(input("Enter offset: "))
    # elif eType == "2":
    #     crypt.encrypt_type = "transpose"
    # elif eType == "3":
    #     crypt.encrypt_type = "plain"

    # Loop to keep the client running until the user enters 'exit'
    while True:
        # Used try block to catch any errors that may occur while running the client
        # This is to prevent the client from crashing
        try:
            # Create a socket object using the socket() function
            # AF_INET is used for IPv4 addresses
            # SOCK_STREAM is used for TCP
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
            # Connect to the server using the connect() function
            # The connect() function takes a tuple of host and port as an argument
            # The host is the IP address of the server and the port is the port number that the server is listening on
            # The client will connect to the server on the same port that the server is listening on
            sock.connect((HOST, PORT))

            # Prompt the user to enter a command
            # The command can be either 'ls', 'cwd', 'dwd', 'upd' or 'exit'
            print('\nuser@{}:{}>'.format(HOST, PORT), sep='', end='')
            # Take in user input and store it in msg. The color of the text is red.
            msg = input(utils.colors['red'])
            msg = msg.lower()  # Convert the message to lowercase
            # Reset the color of the text to default
            print(utils.colors['reset'], end='')

            # If the user enters 'exit', the client will exit and the connection will be closed
            if msg == 'exit':
                print(utils.colors['green'] +
                      'Connection closed'+utils.colors['reset'])
                sock.close()
                break

            # If the user enters 'dwd', the client will download the specified file from the server.
            # The dwd msg, followed by the filepath, will be sent to the server.
            # Corresponding helper functions will be called to download the file.
            # The client will then go back to the prompt to enter another command
            elif msg.startswith('dwd'):
                utils.send_msg(sock, msg)
                utils.client_dwd_helper(sock)
                continue

            # If the user enters 'upd', the client will upload the specified file to the server.
            # The upd msg, followed by the filepath, will be sent to the server.
            # Corresponding helper functions will be called to upload the file.
            # The client will then go back to the prompt to enter another command
            elif msg.startswith('upd'):
                utils.send_msg(sock, msg)
                utils.client_upd_helper(sock, msg)
                continue

            # Here, we just send the message to the server directly, as there is no need for any helper functions
            else:
                utils.send_msg(sock, msg)  # Send the message to the server
                # Receive the message from the server
                msg = utils.recv_msg(sock)
                # Print the message from the server in green
                print(utils.colors['green'] + msg + utils.colors['reset'])

        # If any ConnectionResetError occurs, the client will print Socket and exit
        # ConnectionError could be because the server is not running or the server has closed the connection
        except ConnectionError:
            print(utils.colors['red'] + 'Socket error' + utils.colors['reset'])
            sock.close()
            break
        # If we want to exit the client, we can press Ctrl+C
        # This will raise a KeyboardInterrupt exception
        # The client will print Keyboard Interrupt and exit
        except KeyboardInterrupt:
            print('\nKeyboard interrupt' + utils.colors['reset'])
            sock.close()
            break
