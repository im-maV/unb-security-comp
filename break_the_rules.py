"""
https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html
Ref: Friedman -> https://websites.nku.edu/~christensen/1402%20Friedman%20test%202.pdf
"""

from collections import Counter

from frequencies import FREQ_BY_LANG
from kasiski_test import kasiski_key_length
from test import TEST_CASES
from vigenere import decrypt


def extract_letters(text):
    """Extrai apenas caracteres alfabéticos em minusculo."""
    return "".join(c.lower() for c in text if c.isascii() and c.isalpha())


def calculate_ic(sequence):
    """Calcula o Índice de Coincidência (IC) de uma sequência de caracteres."""
    n = len(sequence)
    if n < 2:
        return 0.0

    counts = Counter(sequence)
    ic = sum(count * (count - 1) for count in counts.values())
    return ic / (n * (n - 1))


def find_key_length(ciphertext, candidates):
    """Estima o tamanho mais provável da chave pelo Método de Friedman"""
    letters = extract_letters(ciphertext)
    best_keylen = candidates[0]
    best_ic = -99999
    top_keylen = []

    for keylen in candidates:
        groups = [[] for _ in range(keylen)]
        for i, l in enumerate(letters):
            groups[i % keylen].append(l)

        avg_ic = sum(calculate_ic(col) for col in groups) / keylen

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


def main():
    cipher_text = """
    Jgo cqfrv wsevx rku yfhqi nfqn qwp gbpx nac twtgf jgo eqk hpot
    ikyihv qpcjdc dta axdobds waqkildoi, okujqxyb uxd cwu fc dcbtdc
    ab lglihu zxp lrgagf qr dta yxcyt hddgnk iz oiuhb zapid aph srq
    jfvso, tymqujd iszjh eszwi hzihi aorkot ecf tzbwjbhd nfjsvqo fc.
    """
    real_key = "QZKMWXPLVB"
    language = TEST_CASES[0]["language"]  # "en" ou "pt"
    freq = FREQ_BY_LANG[language]

    print("[ETAPA 1A] Estimando tamanho da chave via Kasiski")
    letters = extract_letters(cipher_text)
    kasiski_candidates = kasiski_key_length(letters, top_n=10)
    print(f"\n=> Candidatos do Kasiski: {kasiski_candidates}\n")

    print("[ETAPA 1B] Estimando tamanho da chave via IC|Friedman")
    keylen = find_key_length(cipher_text, kasiski_candidates)
    print(f"\n=> Tamanho de chave mais provável: {keylen}\n")

    print(f"\n[ETAPA 2] Reconstruindo chave para tamanho candidato={keylen}")
    key_found = reconstruct_key(cipher_text, keylen, freq)
    print(f"\n=> Chave estimada: '{key_found.upper()}'")
    print(f"\n=> Chave real (gabarito): '{real_key}'")

    plaintext = decrypt(cipher_text, key_found)
    print(f"\n[TEXTO DECIFRADO]\n{plaintext}")


if __name__ == "__main__":
    main()
