import argparse
from pathlib import Path

from frequencies import FREQ_BY_LANG
from break_the_rules.kasiski_test import kasiski_key_length
from tests.test_break_the_rules import TEST_CASES
from vigenere.cipher import decrypt, process_filestream
from break_the_rules.from_file import extract_letters_from_file, reconstruct_key_file, find_key_length_file
from break_the_rules.from_text import extract_letters, reconstruct_key, find_key_length_text



def main(args):
    if args.file:
        file_path = Path(args.file)
        freq = FREQ_BY_LANG[args.language]
        real_key = args.key if args.key else "Não informada"

        print("[ETAPA 1A] Estimando tamanho da chave via Kasiski")
        letters = extract_letters_from_file(file_path)
        kasiski_candidates = kasiski_key_length(letters, top_n=10)
        print(f"\n=> Candidatos do Kasiski: {kasiski_candidates}\n")

        print("[ETAPA 1B] Estimando tamanho da chave via IC|Friedman (streaming)")
        keylen = find_key_length_file(file_path, kasiski_candidates)
        print(f"\n=> Tamanho de chave mais provável: {keylen}\n")

        print(f"\n[ETAPA 2] Reconstruindo chave para tamanho candidato={keylen} (streaming)")
        key_found = reconstruct_key_file(file_path, keylen, freq)
        print(f"\n=> Chave estimada: '{key_found.upper()}'")
        print(f"\n=> Chave real (gabarito): '{real_key}'")

        output_path = file_path.with_name(file_path.stem + "_decrypted" + file_path.suffix)
        process_filestream(file_path, decrypt, key_found, output_path)
        print(f"\n[TEXTO DECIFRADO] escrito em: {output_path}")
        return

    ciphertext = ""
    freq = {}
    real_key = ""
    if args.text:
        ciphertext = args.text
        freq = FREQ_BY_LANG[args.language]
        real_key = args.key if args.key else "Não informada"
    if args.test is not None:
        case = TEST_CASES[args.test]
        ciphertext = case["ciphertext"]
        freq = FREQ_BY_LANG[case["language"]]
        real_key = case["real_key"]

    print("[ETAPA 1A] Estimando tamanho da chave via Kasiski")
    letters = extract_letters(ciphertext)
    kasiski_candidates = kasiski_key_length(letters, top_n=10)
    print(f"\n=> Candidatos do Kasiski: {kasiski_candidates}\n")

    print("[ETAPA 1B] Estimando tamanho da chave via IC|Friedman")
    keylen = find_key_length_text(ciphertext, kasiski_candidates)
    print(f"\n=> Tamanho de chave mais provável: {keylen}\n")

    print(f"\n[ETAPA 2] Reconstruindo chave para tamanho candidato={keylen}")
    key_found = reconstruct_key(ciphertext, keylen, freq)
    print(f"\n=> Chave estimada: '{key_found.upper()}'")
    print(f"\n=> Chave real (gabarito): '{real_key}'")

    plaintext = decrypt(ciphertext, key_found)
    print(f"\n[TEXTO DECIFRADO]\n{plaintext}")


def config_parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "This program recieve a file and/or a plaintext the was encrypt using vigenere cipher."
            "Then the algorithm will try to discover the key length and the key that was used to ecrypt"
            "The language of the text must be informed. Options are: englishe-eng and brazilian-ptbr"
        )
    )

    parser.add_argument("-t", "--text", type=str, help="a small text to ecrypt/decrypt")
    parser.add_argument("-f", "--file", type=str, help="path to a existent file")
    parser.add_argument(
        "-lang", "--language", type=str,
        choices=["ptbr", "en"], help="The language of the text that is encrypt.")
    parser.add_argument("-k", "--key", type=str, help="The real key that was used to encrypt the text.")
    parser.add_argument(
        "--test", type=int,
        help=f"a number correspondent of a INDEX existent test (in test.py file). MAX INDEX: {len(TEST_CASES) - 1}")
    return parser.parse_args()


if __name__ == "__main__":
    args = config_parse_args()
    if not args.file and not args.text and args.test is None:
        print("Either user needs to inform a text and/or a file to be decrypt or a test case INDEX."
              "\nType -h to see how to use the program")
        exit(1)

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_file():
            print("A filepath must be valid and exists.\nType -h to see how to use the program")
            exit(1)
    if (args.file or args.text) and not args.language:
        print("A langauge must be informed.\nType -h to see how to use the program")
        exit(1)

    if args.test is not None and not (0 <= args.test < len(TEST_CASES)):
        print(
            f"Invalid INDEX {args.test} of test case. MAX INDEX: {len(TEST_CASES) - 1}."
            "\nType -h to see how to use the program"
        )
        exit(1)

    main(args)