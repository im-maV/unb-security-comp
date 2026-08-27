import random


def keygen(key_len:int = 14):
    """Gera uma chave aleatoria de bytes"""
    random.seed(1)
    return  bytes([random.randrange(0, 256) for _ in range(key_len)])


def byte_to_hex(data: bytes):
    """Representação legivel em hexadecimal"""
    return " ".join(f"{b:02x}" for b in data)

def encrypt(text: str, key: bytes):
    return _xor_vigenere(text.encode("utf-8"), key)


def decrypt(cipher: bytes, key: bytes) -> str:
    return _xor_vigenere(cipher, key).decode("utf-8")


def _xor_vigenere(data: bytes, key: bytes):
    """Args:
        data: representa ciphertext cifrado ou decifrado
        key: a chave necessario para cifrar/decifrar
    A função realiza uma operação XOR entre o texto (data) e a key. 
    A operação XOR faz o shift da posição da key com a posição do caractere correspondente no ciphertext"""
    if len(key) == 0:
        raise ValueError("Chave não pode ser vazia")
    return bytes(
        b ^ key[i % len(key)]
        for i, b in enumerate(data)
    )


#key = keygen(2)
cipher_text = "Hello!"
key = bytes([0xa1, 0x2f]) # no codigo final a chave sera string, será necessario coverter para bytes
enc_text = encrypt(cipher_text, key)
dec_text = decrypt(enc_text, key)

print(f"chave: {byte_to_hex(key)}\tcifrado: {byte_to_hex(enc_text)}\tdecifrado: {dec_text}")


