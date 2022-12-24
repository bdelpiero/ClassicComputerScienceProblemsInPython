import os
from secrets import token_bytes
from typing import Tuple


def random_key(length: int) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(length)
    # convert those bytes into a bit string and return it
    return int.from_bytes(tb, "big")


def encrypt(original_bytes: bytes) -> Tuple[int, int]:
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR
    return dummy, encrypted


def decrypt(key1: int, key2: int) -> bytes:
    decrypted: int = key1 ^ key2  # XOR
    temp: bytes = int_to_bytes(decrypted)
    return temp


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def encrypt_img(input_file_name: str, output_file_name: str) -> int:
    with open(input_file_name, "rb") as in_file, open(output_file_name, "wb") as out_file:
        key1, key2 = encrypt(in_file.read())
        encrypted_data: bytes = int_to_bytes(key2)
        out_file.write(encrypted_data)
        return key1


def decrypt_img(key: int, input_file_name: str, output_file_name: str):
    with open(input_file_name, "rb") as in_file, open(output_file_name, "wb") as out_file:
        decrypted_data = decrypt(key, int_from_bytes(in_file.read()))
        out_file.write(decrypted_data)


if __name__ == "__main__":
    home_dir = os.path.dirname(os.path.realpath('__file__'))
    files_dir = 'Chapter1/exercise/images'
    input_file_name = os.path.join(home_dir, files_dir + '/alf.jpg')
    encrypted_file_name = os.path.join(home_dir, files_dir + '/encrypted')
    decrypted_file_name = os.path.join(home_dir, files_dir + '/decrypted.jpg')
    key1 = encrypt_img(input_file_name, encrypted_file_name)
    decrypt_img(key1, encrypted_file_name, decrypted_file_name)
