import random
import re
from typing import Literal
import argparse
from argparse import Namespace
from pathlib import Path

from test import TEST_CASES
from collections.abc import Callable


CURRENT_DIR = Path(__file__).parent

def keygen(key_len: int = 20):
    """Gera uma chave pseudoaleatoria de letras maiusculas.
 
    Usa uma seed fixa random.seed(1) para que a chave gerada seja
    sempre a mesma entre execuções facilitando reprodutibilidade
    """
    random.seed(1)
    my_key = ""
    for _ in range(key_len):
        char = random.randrange(65, 91)
        my_key += chr(char)
    return my_key


def _vigenere(text: str, key: str, signal: Literal[1, -1]):
    """Aplica a cifra de Vigenere (cifrando ou decifrando) sobre um texto
 
    Caracteres que não são letras (espaços, pontuação, números, etc.) são
    mantidos inalterados e não avançam o índice da chave
 
    Args:
        text: texto de entrada.
        key: chave usada na cifra/decifra. Apenas letras são consideradas.
        signal: 1 para cifrar e -1 para decifrar.
 
    Returns:
        O texto resultante apos aplicar o deslocamento da cifra
    """
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




def run_test_case(index: int, fallback_key: str) -> None:
    """Executa um caso de teste de TEST_CASES
 
    Cifra o texto do caso de teste, decifra o resultado e confere se o
    texto decifrado bate com o original.
    """
    case = TEST_CASES[index]
    plain_text = case["plain_text"]
    key = case.get("key", fallback_key).upper()
 
    enc = encrypt(plain_text, key)
    dec = decrypt(enc, key)
 
    print(f"\n--- Caso de teste {index} ---")
    print(f"CHAVE ({key})")
    print(f"TEXTO ORIGINAL:\n{plain_text}")
    print(f"TEXTO CIFRADO:\n{enc}")
    print(f"TEXTO DECIFRADO:\n{dec}")
    
    dec = dec.strip()
    plain_text = plain_text.strip()
    assert dec == plain_text, "Falha no round-trip: texto decifrado difere do original!"
    print("\nOK: texto decifrado == texto original")



def process_filestream(
    input_path: Path,
    operation_func: Callable[[str, str], str],
    key: str,
    output_path: Path = CURRENT_DIR / "texts/output.txt",
):
    """Lê um arquivo linha a linha, aplica ``operation_func`` e grava o resultado."""
    
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            processed_line = operation_func(line, key)
            outfile.write(processed_line)
    print(f"Arquivo gerado {output_path}")



def main(args: Namespace):
    """
    Suporta três modos, que podem ser combinados na mesma execução:
        - args.text: cifra/decifra um texto informado
        - args.file: cifra/decifra o conteúdo de um arquivo
        - args.test: executa um caso de teste pré-definido
    """

    key = args.key.upper() if args.key else keygen()
    print(f"CHAVE ({key})")

    operations_func: dict[str, Callable[[str, str], str]] = {
        "encrypt": encrypt,
        "decrypt": decrypt,
    }

    operation_func = operations_func[args.operation]
    if args.file:
        file_path = Path(args.file)
        output_path = CURRENT_DIR / f"texts/output_{args.operation}.txt"
        process_filestream(file_path, operation_func, key, output_path)

    if args.text:
        result = operation_func(args.text, key)
        print(f"RESULTADO ({args.operation}): {result}")

    if args.test is not None:
        run_test_case(args.test, fallback_key=key)



def config_parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "this program recieve a file and/or a plaintext to encrypt using vigenere cipher."
            "A key could be given to encrypt."
            "if not, then a random key of 14 legth it will be random generated"
        )
    )
    parser.add_argument(
        "-op", "--operation", required=True, choices=["encrypt", "decrypt"], 
        default="encrypt", type=str, 
        help="the operation to perform, either encrypt or decrypt")
    parser.add_argument("-k", "--key", type=str, help="a key that will be used to encrypt the plaintext")
    parser.add_argument("-t",  "--text", type=str, help="a small text to ecrypt/decrypt")
    parser.add_argument("-f", "--file", type=str, help="path to a existent file")
    parser.add_argument(
        "--test", type=int, 
        help=f"a number correspondent of a INDEX existent test (in test.py file). MAX INDEX: {len(TEST_CASES) - 1}")
    return parser.parse_args()


if __name__ == "__main__":
    args = config_parse_args()
    if not args.file and not args.text and args.test is None:
        print("Either user needs to inform a text and/or a file to be encrypt or a test case INDEX."
              "\nType -h to see how to use the program")
        exit(1)

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_file():
            print("A filepath must be valid and exists.\nType -h to see how to use the program")
            exit(1)

    if args.test is not None and not (0 <= args.test < len(TEST_CASES)):
        print(
            f"Invalid INDEX {args.test} of test case. MAX INDEX: {len(TEST_CASES) - 1}."
            "\nType -h to see how to use the program"
        )
        exit(1)

    main(args)
