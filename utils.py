# This is the helper utils.py file for the server and client
# It contains all the functions that are used by both the server and client

import os  # for os.path
import encryption as crypt  # Path: encryption.py

HOST = ''
PORT = 4040
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # 4KB of buffer size for each file chunk
PATH = os.getcwd()  # Path to the current directory

# Color codes (ANSI) for printing
colors = {
    'reset': f"\033[0m",
    'red': f"\033[31m",
    'blue': f"\033[34m",
    'green': f"\033[32m",
}


def recv_msg(sock):
    """ Wait for data to arrive on the socket, then parse into
    messages using b'\0' as message delimiter """
    data = bytearray()
    msg = ''
    # Repeatedly read 4096 bytes off the socket, storing the bytes
    # in data until we see a delimiter
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            # Socket has been closed prematurely
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            # we know from our protocol rules that we only send
            # one message per connection, so b'\0' will always be
            # the last character
            msg = data.rstrip(b'\0')
    # Decode the message from bytes to a string and then decrypt it
    msg = crypt.decrypt(msg.decode('utf-8'))
    return msg


def prep_msg(msg):
    """ Prepare a string to be sent as a message """
    # Encrypt the message
    msg = crypt.encrypt(msg)
    msg += '\0'
    return msg.encode('utf-8')  # convert to bytes


def send_msg(sock, msg):
    """ Send a string over a socket, preparing it first """
    data = prep_msg(msg)
    sock.sendall(data)


def CWD(sock):
    """ Current Working Directory """
    cwd = os.getcwd()
    send_msg(sock, cwd)


def LS(sock):
    """ List files in current directory """
    files = ""
    path = os.getcwd()
    for file in os.listdir(path):
        files += file + "    "  # Spaces for formatting
    if files == "":
        files = "Directory is empty"  # If directory is empty, print this
    send_msg(sock, files)


def CD(sock, msg):
    """ Change directory """
    path = msg[3:]  # Get the path from the message
    try:
        if path == "~":
            os.chdir(PATH)  # Change to the root directory if path is ~
        else:
            os.chdir(path)
        send_msg(sock, "OK")
    # If the path is invalid, send NOK
    except:
        send_msg(sock, "NOK")


def DWD(sock, msg):
    """ Download file """
    filepath = msg[4:]  # Get the path from the message
    try:
        filename = os.path.basename(filepath)  # Get the filename
        filesize = os.path.getsize(filepath)  # Get the filesize
        # Send the filename and filesize
        sock.send(crypt.encrypt(
            f"{filename}{SEPARATOR}{filesize}").encode("utf-8"))

        # Loop through the file and send it chunk by chunk of size BUFFER_SIZE
        with open(filepath, "r") as f:
            print("Sending file...")
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                # Encrypt the data and send it
                sock.sendall(crypt.encrypt(data).encode("utf-8"))
        print("File sent")
    # If the file is not found, send NOK or if there is an error during sending
    except:
        send_msg(sock, "NOK")
    finally:
        return


def UPD(sock):
    """ Upload file """
    try:
        received = crypt.decrypt(sock.recv(BUFFER_SIZE).decode(
            "utf-8"))  # Receive the filename and filesize
        # Split the filename and filesize
        filename, filesize = received.split(SEPARATOR)
        filesize = int(filesize)
        with open(filename, "w") as f:
            print("Receiving file...")
            while True:
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                # Write the data to the file after decrypting it
                f.write(crypt.decrypt(bytes_read.decode("utf-8")))
        sock.close()
        print("File received")
    except:
        send_msg(sock, "NOK")
    finally:
        return


def client_dwd_helper(sock):
    """Helper function for client DWD command"""
    try:
        received = crypt.decrypt(sock.recv(BUFFER_SIZE).decode("utf-8"))
        filepath, filesize = received.split(SEPARATOR)
        filesize = int(filesize)
        filename = os.path.basename(filepath)
        with open(filename, "w") as f:
            print("Receiving file...")
            while True:
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(crypt.decrypt(bytes_read.decode("utf-8")))
        print("File downloaded successfully")
    except:
        print("File not found")
    finally:
        sock.close()
        return


def client_upd_helper(sock, msg):
    """Helper function for client UPD command"""
    filepath = msg[4:]
    try:
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        sock.send(crypt.encrypt(
            f"{filename}{SEPARATOR}{filesize}").encode("utf-8"))
        with open(filepath, "r") as f:
            print("Sending file...")
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                sock.sendall(crypt.encrypt(data).encode("utf-8"))
        print("File uploaded successfully")
    except:
        print("File not found")
    finally:
        sock.close()
    return
