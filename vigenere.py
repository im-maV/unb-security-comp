import random
import re
from typing import Literal

from test import TEST_CASES


def keygen(key_len: int = 14):
    random.seed(1)
    my_key = ""
    for _ in range(key_len):
        char = random.randrange(97, 123)
        my_key += chr(char)
    return my_key


def _vigenere(text: str, key: str, signal: Literal[1, -1]):
    # sinal é +1 para cifrar e -1 para decifrar
    output = []
    key_idx = 0
    for i in range(len(text)):
        if not re.match(r"[a-zA-Z]", text[i]):
            output.append(text[i])
            continue

        is_upper = text[i].isupper()
        char_pos = (ord(text[i].lower()) - 97) % 26
        key_char_pos = (ord(key[key_idx % len(key)].lower()) - 97) % 26
        # deslocamento
        shift = (char_pos + (signal * key_char_pos)) % 26
        new_char = chr(shift + 97)

        if is_upper:
            new_char = new_char.upper()
        output.append(new_char)
        key_idx += 1
    return "".join(output)


def encrypt(text: str, key: str):
    return _vigenere(text, key, signal=1)


def decrypt(text: str, key: str):
    return _vigenere(text, key, signal=-1)


def main():
    case = TEST_CASES[0]
    plain_text = case["plain_text"]
    key = "QZKMWXPLVB"

    enc = encrypt(plain_text, key)
    dec = decrypt(enc, key)
    print(f"CHAVE ({key.upper()})")
    print("\nTEXTO CIFRADO:")
    print(enc.strip())
    print("\nTEXTO DECIFRADO:")
    print(dec.strip())


if __name__ == "__main__":
    main()
