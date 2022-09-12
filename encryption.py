ENCRYPT_TYPE = "substitute"
OFFSET = 2


def encrypt(msg, mode=ENCRYPT_TYPE):
    """ Encrypt message """
    if mode == "substitute":
        return substitute(msg, OFFSET)
    elif mode == "transpose":
        return transpose(msg)
    else:
        return msg


def substitute(msg, offset=OFFSET):
    """ Caesar cipher """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_msg = ""
    for char in msg:
        if char in alphabet:
            new_msg += alphabet[(alphabet.index(char) + offset) % 26]
        else:
            new_msg += char
    return new_msg


def transpose(msg):
    """ Transpose cipher """
    return msg[::-1]


def decrypt(msg, mode=ENCRYPT_TYPE):
    """ Decrypt message """
    if mode == "substitute":
        return substitute(msg, -OFFSET)
    elif mode == "transpose":
        return transpose(msg)
    else:
        return msg
