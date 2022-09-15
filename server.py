# This is the server side of the program

import socket  # For sockets

import utils  # Path: utils.py

# Default host and port
HOST = ''
PORT = 4040

# Create a TCP socket object for the server to listen on


def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse the socket for multiple connections
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))  # Bind the server to the host and port
    # Set a timeout for the socket, so that the server can check for keyboard interrupts
    sock.settimeout(5)
    sock.listen(100)  # Listen for up to 100 connections
    return sock

# After the connection is established, the server will receive the message from the client


def handle_client(sock, addr):
    """ Receive data from the client via sock """
    # try block to catch any errors that may occur while handling the client connection
    try:
        # Loop to keep the server running until the user enters 'exit'
        while True:
            # Receive the message from the client
            # Convert the message to lowercase
            msg = utils.recv_msg(sock)
            msg = msg.lower()
            # Print the message from client in the server terminal
            print('Received message: ' + msg)

            # Based on the value of msg, the server will perform the corresponding action
            # i.e. will call the corresponding functions
            # CWD - Current working directory
            if(msg == "cwd"):
                utils.CWD(sock)
            # LS - List files in the current directory
            elif(msg == "ls"):
                utils.LS(sock)
            # CD - Change directory
            elif(msg.startswith("cd")):
                utils.CD(sock, msg)
            # DWD - Download file from the server
            elif(msg.startswith("dwd")):
                utils.DWD(sock, msg)
                sock.close()
                break
            # UPD - Upload file to the server
            elif(msg.startswith("upd")):
                utils.UPD(sock)
                sock.close()
                break
            # EXIT - Exit the server
            elif(msg == "exit"):
                print("Closing connection")
                sock.close()
                break
            # If the user enters an invalid command, the server will send Invalid command
            else:
                utils.send_msg(sock, "Invalid command")
                continue
    # If any error occurs, the server will print out the error message
    except (ConnectionError, BrokenPipeError) as err:
        print(err)


# Main function
if __name__ == '__main__':
    # Create a socket object for the server to listen on
    listen_sock = create_listen_socket(HOST, PORT)
    # get the address of the server
    addr = listen_sock.getsockname()
    # Print the address of the server
    print('Listening on {}'.format(addr))
    try:
        # Loop to keep the server checking for new connections
        while True:
            try:
                client_sock, addr = listen_sock.accept()
                print('Connection from {}'.format(addr))
                handle_client(client_sock, addr)
            # If the server times out, it will check for keyboard interrupts
            # And if there is none it will continue to check for new connections
            except socket.timeout:
                print('Timed out, listening again')
    # If the user enters Ctrl+C, the server will close the socket and exit
    except KeyboardInterrupt:
        print('Keyboard interrupt, killing server')
    listen_sock.close()
