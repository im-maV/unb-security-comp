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
from vigenere import decrypt, process_filestream

CURRENT_DIR = Path(__file__).parent
CHUNK_SIZE = 65536  # 64KB por leitura


def iter_letters_from_file(file_path, chunk_size=CHUNK_SIZE):
    """Gera as letras minúsculas do arquivo uma a uma lendo em blocos

    Usada para montar a sequência de letras necessária ao teste de Kasiski."""
    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for char in chunk:
                c = char.lower()
                if "a" <= c <= "z":
                    yield c


def extract_letters_from_file(file_path: Path, chunk_size=CHUNK_SIZE):
    """Monta a string de letras do arquivo lendo-o em blocos, em vez de dar
    um único f.read() no arquivo inteiro
    """
    return "".join(iter_letters_from_file(file_path, chunk_size))


def extract_letters(text: str):
    """Extrai apenas caracteres alfabéticos em minusculo"""
    return "".join(c.lower() for c in text if c.isascii() and c.isalpha())


def calculate_ic(counts: Counter, n: int):
    """Calcula o Indice de Coincidência (IC) a partir de um Counter de frequências
    1/n(n-1) * ∑fi * (fi-1)

    Args: 
    - counts: dicionario `letra:contagem` representando a quantidade de vezes que determinada letra 
    apareceu em uma coluna para um certa key length
    - n: quantidade de letras presentes na coluna (tamanho do array column)



    """
    if n < 2:
        return 0.0
    ic = sum(count * (count - 1) for count in counts.values())
    return ic / (n * (n - 1))


def get_column_freq_from_text(text: str, keylen: int) -> tuple[list[Counter], list[int]]:
    """Agrupa as letras do texto nas `keylen` colunas e retorna (counters, lengths).
    Para um certo valor `keylen` gera-se `keylen` colunas, onde cada uma aramzena letras de uma certa posição da chave
    
    Args:
    - text: texto cifrado
    - keylen: determinado tamanho da chave

    return:
    - counters: array de colunas, onde cada uma contem dicionarios letra:contagem das letras presentes naquela coluna
    - lenghts: array com tamanho de cada coluna
    """
    letters = extract_letters(text)
    counters = [Counter() for _ in range(keylen)]
    lengths = [0] * keylen
    for i, l in enumerate(letters):
        col = i % keylen
        counters[col][l] += 1
        lengths[col] += 1
    return counters, lengths



def get_column_freq_from_file(file_path: Path, keylen: str, chunk_size=CHUNK_SIZE):
    """Le o arquivo em blocos e conta a frequência de letras por coluna,
    sem carregar o texto inteiro na memória.
    
    Cria-se `keylen` colunas, onde cada uma aramzena letras de uma certa posição da chave
    Args:
        - file_path: path para um arquivo
        - keylen: determinado tamanho da chave
        - chunk_size: quantida de bytes a ser lido do arquivo
    
        return:
        - counters: array de colunas, onde cada uma contem dicionarios letra:contagem das letras presentes naquela coluna
        - lenghts: array com tamanho de cada coluna
    """
    counters = [Counter() for _ in range(keylen)]
    lengths = [0] * keylen
    idx = 0

    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for char in chunk:
                c = char.lower()
                if "a" <= c <= "z":
                    col = idx % keylen
                    counters[col][c] += 1
                    lengths[col] += 1
                    idx += 1

    return counters, lengths





def find_key_length_text(ciphertext, candidates):
    """Estima o tamanho mais provável da chave pelo Método de Friedman -IC"""
    if len(candidates) == 0:
        candidates = [i for i in range(2, 21)]
    columns_by_candidate = {
        keylen: get_column_freq_from_text(ciphertext, keylen) for keylen in candidates
    }
    return find_key_length_from_columns(columns_by_candidate)


def find_key_length_file(file_path : Path, candidates: list[int], chunk_size=CHUNK_SIZE):
    """Estima o tamanho mais provável da chave pelo Método de Friedman -IC"""
    if len(candidates) == 0:
        candidates = [i for i in range(2, 21)]

    columns_by_candidate = {
        keylen: get_column_freq_from_file(file_path, keylen, chunk_size) for keylen in candidates
    }
    return find_key_length_from_columns(columns_by_candidate)




def find_key_length_from_columns(columns_by_candidate: dict[int, tuple[list[Counter], list[int]]]):
    """Recebe um dicionário contendo todos os `keylen` mais provávies.
    Para cada `keylen` cadidadto com suas colunas onde cada uma contem 
    apenas letras de determinada posição cifrada por uma letra da chave,
    realiza-se o cálculo do IC para cada coluna (a média é tirada no final).

    Se o IC for um valor próximo ao um valor não uniforme de algum alfabeto (ex: 0.065 no ingles), então
    é provável que o `keylen` atual seja o verdadeiro

    Args:
    -columns_by_candidate: um dicionario `keylen`(int): tuple[lista de colunas; tamanho das colunas]
    return:
    - array ordenado do maior para o menor, contendo a `keylen` e seu respectivo IC

    """
    best_keylen = None
    best_ic = -99999
    top_keylen = []

    for keylen, (counters, lengths) in columns_by_candidate.items():
        avg_ic = sum(
            calculate_ic(counters[i], lengths[i]) for i in range(keylen)
        ) / keylen

        print(f"[Friedman] tamanho={keylen} IC_medio={avg_ic:.5f}")  # debug visual

        if avg_ic > best_ic:
            best_ic = avg_ic
            best_keylen = keylen

        top_keylen.append((keylen, avg_ic))

    top_keylen.sort(key=lambda x: x[1], reverse=True)
    print(f"\n=> Candidatos ordenados por IC médio: {top_keylen}")

    return best_keylen




def analyze_column_shift(counts: Counter, n: int, alphabet_freq: dict[str, float]):
    """Calcula a correlação de frequências (IC Mútuo) para os 26 deslocamentos possiveis,
    a partir das CONTAGENS de uma coluna 
    
    Args:
    -counts: dict letra:contagem

    """
    if n == 0:
        return [(0.0, 0)]

    q = [counts.get(chr(97 + i), 0) / n for i in range(26)]
    p = [alphabet_freq[chr(97 + i)] for i in range(26)]

    keychar_candidates = []
    for shift in range(26):
        m = sum(p[i] * q[(i + shift) % 26] for i in range(26))
        keychar_candidates.append((m, shift))

    keychar_candidates.sort(reverse=True)
    return keychar_candidates



def reconstruct_key(ciphertext: str, keylen: int, alphabet_freq: dict[str, float]):
    """Reconstrói a chave analisando umm arquivo de texto simples """
    counters, lengths = get_column_freq_from_text(ciphertext, keylen)
    return reconstruct_key_from_columns(counters, lengths, alphabet_freq)


def reconstruct_key_file(file_path: Path, keylen: int, alphabet_freq: dict[str, float], chunk_size=CHUNK_SIZE):
    """lê o arquivo em blocos para montar as
    contagens por coluna, sem carregar o texto inteiro na memoria"""
    counters, lengths = get_column_freq_from_file(file_path, keylen, chunk_size)
    return reconstruct_key_from_columns(counters, lengths, alphabet_freq)



def reconstruct_key_from_columns(counters: list[Counter], lengths: list[int], alphabet_freq: dict[str, float]):
    """Reconstrói a chave analisando cada grupo (coluna) individualmente.
        Colunas são grupos de caracteres que foram cifrados pelo mesmo caractere da chave (cifra de césar)

    Args: 
    - counters: list de dict letras:contagem simbolizando as colunas
    - lengths: tamanho de cada coluna
    - alphabet_freq: frequencia de cada letra de determinado alfaberto
    return:
    - possivel chave
    """
    key_chars = []
    for idx, (counts, n) in enumerate(zip(counters, lengths)):
        candidates = analyze_column_shift(counts, n, alphabet_freq)
        best_m, best_shift = candidates[0]
        key_char = chr(97 + best_shift)
        key_chars.append(key_char)

        print(
            f"grupo {idx} (n={n}) -> shift={best_shift} letra='{key_char}' M={best_m:.5f}"
        )

    return "".join(key_chars)




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
        choices=["ptbr", "eng"], help="The language of the text that is encrypt.")
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
