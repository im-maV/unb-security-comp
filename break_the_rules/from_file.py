from collections import Counter
from pathlib import Path
from break_the_rules.key_reconstruction import find_key_length_from_columns, reconstruct_key_from_columns

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



def find_key_length_file(file_path : Path, candidates: list[int], ic_lang:float, chunk_size=CHUNK_SIZE):
    """Estima o tamanho mais provável da chave pelo Método de Friedman -IC"""
    if len(candidates) == 0:
        candidates = [i for i in range(2, 21)]

    columns_by_candidate = {
        keylen: get_column_freq_from_file(file_path, keylen, chunk_size) for keylen in candidates
    }
    ranked = find_key_length_from_columns(columns_by_candidate, ic_lang)
    return ranked, columns_by_candidate



def reconstruct_key_file(file_path: Path, keylen: int, alphabet_freq: dict[str, float], chunk_size=CHUNK_SIZE):
    """lê o arquivo em blocos para montar as
    contagens por coluna, sem carregar o texto inteiro na memoria"""
    counters, lengths = get_column_freq_from_file(file_path, keylen, chunk_size)
    return reconstruct_key_from_columns(counters, lengths, alphabet_freq)