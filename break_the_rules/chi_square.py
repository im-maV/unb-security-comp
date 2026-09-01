from collections import Counter
from break_the_rules.key_reconstruction import reconstruct_key_from_columns

def chi_squared_from_column_counters(counters: list[Counter], shifts: list[int],
                                       alphabet_freq: dict, n_total: int) -> float:
    print(f"SHIFTERS: {shifts}")
    decrypted_counts = Counter()
    for counts_j, shift_j in zip(counters, shifts):
        for cifrado_idx in range(26):
            letra_cifrada = chr(97 + cifrado_idx)
            qtd = counts_j.get(letra_cifrada, 0)
            if qtd:
                letra_decifrada = chr(97 + (cifrado_idx - shift_j) % 26)
                decrypted_counts[letra_decifrada] += qtd  # <- nao decrypted_counts[letra_cifrada]

    score = 0.0
    for letra, freq_esperada in alphabet_freq.items():
        observado = decrypted_counts.get(letra, 0)
        esperado = freq_esperada * n_total
        score += (observado - esperado) ** 2 / esperado
    return score



def select_keylen_by_chisquare(columns_by_candidate, ranked, alphabet_freq, top_n=5):
    scored = []
    for keylen, avg_ic, diff in ranked[:top_n]:
        counters, lengths = columns_by_candidate[keylen]
        key, shifts = reconstruct_key_from_columns(counters, lengths, alphabet_freq, return_shifts=True)
        n_total = sum(lengths)
        score = chi_squared_from_column_counters(counters, shifts, alphabet_freq, n_total)
        print(f"[Chi2] keylen={keylen} chave='{key.upper()}' score={score:.4f}")
        scored.append((keylen, key, score))

    scored.sort(key=lambda x: x[2])
    print(f"\n=> Candidatos ordenados por qui-quadrado: "
          f"{[(k, key.upper(), round(s,2)) for k, key, s in scored]}")

    best_keylen, best_key, _ = scored[0]
    return best_keylen, best_key, scored