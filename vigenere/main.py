
import argparse
from argparse import Namespace
from pathlib import Path
from vigenere.cipher import decrypt, encrypt, process_filestream, run_test_case, keygen

from tests.test_vigenere import TEST_CASES
from collections.abc import Callable

CURRENT_DIR = Path(__file__).parent




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
        output_path = CURRENT_DIR.parent / f"outputs/output_{args.operation}.txt"
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

    if args.operation == "decrypt" and (args.file or args.text) and not args.key:
        print("A key must be passed when decrypting a file/text."
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
