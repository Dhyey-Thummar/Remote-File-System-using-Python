# This file is for the encryption and decryption of messages
# It contains the functions for encrypting and decrypting messages
# Acts as the encryption layer in the network stack
ENCRYPT_TYPE = "transpose"
OFFSET = 2

# Call the correct function based on the encryption type
def encrypt(msg, mode=ENCRYPT_TYPE):
    """ Encrypt message """
    if mode == "substitute":
        return substitute(msg, OFFSET)
    elif mode == "transpose":
        return transpose(msg)
    else:
        return msg

# Substitute cipher
def substitute(msg, offset=OFFSET):
    """ Caesar cipher """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_msg = ""
    for char in msg:
        if char in alphabet:
            # Get the index of the character in the alphabet
            # Add the offset to the index
            # Modulo the index by 26 to get the index of the new character
            # Add the new character to the new message
            new_msg += alphabet[(alphabet.index(char) + offset) % 26]
        else:
            new_msg += char
    return new_msg


def transpose(msg):
    """ Transpose cipher """
    return msg[::-1]  # Reverse the message


def decrypt(msg, mode=ENCRYPT_TYPE):
    """ Decrypt message """
    if mode == "substitute":
        return substitute(msg, -OFFSET)  # Subtract the offset to decrypt
    elif mode == "transpose":
        return transpose(msg)  # Reverse the message to decrypt
    else:
        return msg
