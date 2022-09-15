# Simple Remote File Service (RFS) using socket programming in Python

This is a simple file service that supports the following operations:

- `ls` - list files in the current directory
- `cwd` - get the current working directory
- `cd <filepath>` - change the current working directory to the specified path
- `dwd <filepath>` - download the specified file from the server
- `upd <filepath>` - upload the specified file to the server

## Underlying Architecture

Layered architecture is used to implement the file service. The following diagram shows the layers and their interactions.

Layer | Description | Scripts
--- | --- | ---
File Service | The file service layer is the top layer. It is responsible for handling the client requests and sending the appropriate responses. | [client.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/client.py), [server.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/server.py)
Crypto Service | The crypto service layer is responsible for encrypting and decrypting the data sent between the client and the server. | [encryption.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/encryption.py)
Networking | The networking layer is responsible for sending and receiving data over the network. | [utils.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/utils.py)

## Instructions to setup and run the service.

### Setup :

1. Clone the repository
2. No additional setup is required.

### Running the service :

1. Run the [server.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/server.py) file to start the server.
2. Run the [client.py](https://github.com/Dhyey-Thummar/Remote-File-System-using-Python/blob/master/client.py) file to start the client.
3. The client will prompt you to enter the command. Enter the command and press enter to send the command to the server.

#

