"""
https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html
Ref: Friedman -> https://websites.nku.edu/~christensen/1402%20Friedman%20test%202.pdf
"""

from collections import Counter
import argparse
from pathlib import Path

from frequencies import FREQ_BY_LANG
from kasiski_test import kasiski_key_length
from tests.test_break_the_rules import TEST_CASES
from vigenere import decrypt

CURRENT_DIR = Path(__file__).parent


def extract_letters(text):
    """Extrai apenas caracteres alfabéticos em minusculo."""
    return "".join(c.lower() for c in text if c.isascii() and c.isalpha())


def calculate_ic(column_counter, column_len):
    """Calcula o Índice de Coincidência (IC) de uma sequência de caracteres."""
    if column_len < 2:
        return 0.0

    ic = sum(count * (count - 1) for count in column_counter.values())
    return ic / (column_len * (column_len - 1))



def get_column_freq_file(filetext, keylen):
    """Lê um arquivo em blocos e atualiza os contadores coluna por coluna."""
    chunk_size = 65536  # 64kb
    column_lengths = [0] * keylen
    column_counters = [Counter() for _ in range(keylen)]
    
    # Mantém o índice global de letras válidas para o operador '%' funcionar entre blocos
    global_letter_idx = 0 
    
    with open(filetext, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
                
            letters = extract_letters(chunk)
            for char in letters:
                col = global_letter_idx % keylen
                column_counters[col][char] += 1
                column_lengths[col] += 1
                global_letter_idx += 1
        
    return column_counters, column_lengths


def get_column_freq_text(ciphertext, keylen):
    """Processa uma string que já está inteira na memória RAM."""
    column_lengths = [0] * keylen
    letters = extract_letters(ciphertext)
    column_counters = [Counter() for _ in range(keylen)]
    
    for i, char in enumerate(letters):
        col = i % keylen
        column_counters[col][char] += 1
        column_lengths[col] += 1

    return column_counters, column_lengths


def find_key_length(ciphertext, candidates, is_file=False):
    """Estima o tamanho mais provável da chave pelo Método de Friedman."""
    best_keylen = candidates[0]
    best_ic = -99999
    top_keylen = []

    for keylen in candidates:
        # Verifica se a entrada é um caminho de arquivo ou uma string de texto
        if is_file:
            column_counters, column_lengths = get_column_freq_file(ciphertext, keylen)
        else:
            column_counters, column_lengths = get_column_freq_text(ciphertext, keylen)

        avg_ic = sum(calculate_ic(column_counters[i], column_lengths[i]) for i in range(keylen)) / keylen

        print(f"[Friedman] tamanho={keylen} IC_medio={avg_ic:.5f}")  # debug visual

        if avg_ic > best_ic:
            best_ic = avg_ic
            best_keylen = keylen

        top_keylen.append((keylen, avg_ic))

    top_keylen.sort(key=lambda x: x[1], reverse=True)
    print(f"\n=> Candidatos ordenados por IC médio: {top_keylen}")

    return best_keylen


def analyze_group_shift(group, alphabet_freq):
    """Calcula a correlação de frequências (Índice de Coincidência Mútuo) para os 26 deslocamentos."""
    n = len(group)
    if n == 0:
        return [(0.0, 0)]

    counts = Counter(group)
    q = [counts.get(chr(97 + i), 0) / n for i in range(26)]
    p = [alphabet_freq[chr(97 + i)] for i in range(26)]

    keychar_candidates = []
    for shift in range(26):
        m = sum(p[i] * q[(i + shift) % 26] for i in range(26))
        keychar_candidates.append((m, shift))

    keychar_candidates.sort(reverse=True)
    return keychar_candidates


def reconstruct_key(ciphertext, keylen, alphabet_freq):
    """Reconstrói a chave analisando cada grupo individualmente."""
    letters = extract_letters(ciphertext)
    cesar_groups = [[] for _ in range(keylen)]

    for idx, l in enumerate(letters):
        cesar_groups[idx % keylen].append(l)

    key_chars = []
    for idx, group in enumerate(cesar_groups):
        candidates = analyze_group_shift(group, alphabet_freq)
        best_m, best_shift = candidates[0]
        key_char = chr(97 + best_shift)
        key_chars.append(key_char)

        print(
            f"grupo {idx} (n={len(group)}) -> shift={best_shift} letra='{key_char}' M={best_m:.5f}"
        )

    return "".join(key_chars)


def run_test_case(index: int):
    """Executa um caso de teste de TEST_CASES
    """
    case = TEST_CASES[index]
    ciphertext = case["ciphertext"]
    freq = FREQ_BY_LANG[case["language"]]
 
    print("[ETAPA 1A] Estimando tamanho da chave via Kasiski")
    letters = extract_letters(args.text)
    kasiski_candidates = kasiski_key_length(letters, top_n=10)
    print(f"\n=> Candidatos do Kasiski: {kasiski_candidates}\n")

    print("[ETAPA 1B] Estimando tamanho da chave via IC|Friedman")
    keylen = find_key_length(args.text, kasiski_candidates)
    print(f"\n=> Tamanho de chave mais provável: {keylen}\n")

    print(f"\n[ETAPA 2] Reconstruindo chave para tamanho candidato={keylen}")
    key_found = reconstruct_key(args.text, keylen, freq)
    print(f"\n=> Chave estimada: '{key_found.upper()}'")
    print(f"\n=> Chave real (gabarito): '{real_key}'")

    plaintext = decrypt(args.text, key_found)
    print(f"\n[TEXTO DECIFRADO]\n{plaintext}")
    
    
    dec = dec.strip()
    plain_text = plain_text.strip()
    assert dec == plain_text, "Falha no round-trip: texto decifrado difere do original!"
    print("\nOK: texto decifrado == texto original")




def main(args):

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


    print("[ETAPA 1A] Estimando tamanho da chave via Kasiski")
    letters = extract_letters(ciphertext)
    kasiski_candidates = kasiski_key_length(letters, top_n=10)
    print(f"\n=> Candidatos do Kasiski: {kasiski_candidates}\n")

    print("[ETAPA 1B] Estimando tamanho da chave via IC|Friedman")
    keylen = find_key_length(ciphertext, kasiski_candidates)
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

    parser.add_argument("-t",  "--text", type=str, help="a small text to ecrypt/decrypt")
    parser.add_argument("-f", "--file", type=str, help="path to a existent file")
    parser.add_argument(
        "-lang", "--language", type=str, 
        choices=["ptbr", "eng"], help="The language of the text that is encrypt.")
    parser.add_argument("-k", "--key", type=str,  help="The real key that was used to encrypt the text.")
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
