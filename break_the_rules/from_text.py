from collections import Counter
from break_the_rules.key_reconstruction import find_key_length_from_columns, reconstruct_key_from_columns

def extract_letters(text: str):
    """Extrai apenas caracteres alfabéticos em minusculo"""
    return "".join(c.lower() for c in text if c.isascii() and c.isalpha())


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



def find_key_length_text(ciphertext: str, candidates: list[int], ic_lang: float):
    """Estima o tamanho mais provável da chave pelo Método de Friedman -IC"""
    if len(candidates) == 0:
        candidates = [i for i in range(2, 21)]
    columns_by_candidate = {
        keylen: get_column_freq_from_text(ciphertext, keylen) for keylen in candidates
    }
    ranked = find_key_length_from_columns(columns_by_candidate, ic_lang)
    return ranked, columns_by_candidate


def reconstruct_key(ciphertext: str, keylen: int, alphabet_freq: dict[str, float]):
    """Reconstrói a chave analisando umm arquivo de texto simples """
    counters, lengths = get_column_freq_from_text(ciphertext, keylen)
    return reconstruct_key_from_columns(counters, lengths, alphabet_freq)
