"""
https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Kasiski.html
The Kasiski Test -> https://www.researchgate.net/publication/337338002_Analyzing_the_Kasiski_Method_Against_Vigenere_Cipher
"""

from collections import Counter
from itertools import combinations


def find_repeated_sequences(letters, seq_len):
    """Encontrar todos os cryptogramas repetidos no texto codificado."""
    positions = {}

    for i in range(len(letters) - seq_len + 1):
        seq = letters[i : i + seq_len]
        positions.setdefault(seq, []).append(i)

    return {seq: pos for seq, pos in positions.items() if len(pos) > 1}


def kasiski_distances(repeats):
    """Calcular a distância entre os cryptogramas repetidos."""
    distances = []

    for pos_list in repeats.values():
        for a, b in combinations(pos_list, 2):
            distances.append(b - a)
    return distances


def kasiski_key_length(ciphertext, seq_len=3, k_min=2, k_max=20, top_n=3):
    """Calcula todos os fatores (divisores) das distâncias entre repetiçõese devolve os tamanhos de chave mais votados."""
    # seq_len=3 é o padrão clássico do método de Kasiski (trigramas) sequências mais curtas (2) geram repetições por acaso demais;
    # mais longas (4+) costumam ser raras em textos curtos. Pode ser ajustado se o texto for muito longo/curto, mas 3 é o valor de
    # referência da literatura.

    repeats = find_repeated_sequences(ciphertext, seq_len)
    if not repeats:
        print(f"[Kasiski] nenhuma sequência de tamanho {seq_len} se repetiu no texto")
        return []

    distances = kasiski_distances(repeats)

    factor_votes = Counter()
    for d in distances:
        for f in range(k_min, k_max + 1):
            if d % f == 0:
                factor_votes[f] += 1

    if not factor_votes:
        return []

    ordered_votes = sorted(factor_votes.items(), key=lambda item: item[1], reverse=True)
    for keylen, votes in ordered_votes:
        print(f"[Kasiski] tamanho={keylen} votos={votes}")

    return [keylen for keylen, _votos in ordered_votes]
