"""
https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html
Ref: Friedman -> https://websites.nku.edu/~christensen/1402%20Friedman%20test%202.pdf
"""

from collections import Counter


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




