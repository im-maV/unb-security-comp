"""
https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html
Ref: Friedman -> https://websites.nku.edu/~christensen/1402%20Friedman%20test%202.pdf
Kasiski attack
"""

from vigenere import decrypt
from collections import Counter
from frequencies import FREQ_EN, FREQ_PT


def extract_letters(text):
    """Extrai apenas caracteres alfabéticos em minusculo."""
    return "".join(c.lower() for c in text if c.isascii() and c.isalpha())


def calculate_ic(sequence):
    """Calcula o Índice de Coincidência (IC) de uma sequência de caracteres."""
    n = len(sequence)
    if n < 2:
        return 0.0

    counts = Counter(sequence)
    ic = sum(count * (count-1) for count in counts.values())
    return ic / (n * (n-1))

def find_key_length(ciphertext, k_min, k_max):
    """Estima o tamanho mais provável da chave pelo Método de Friedman"""
    letters = extract_letters(ciphertext)
    best_keylen = k_min
    best_ic = -99999

    for keylen in range(k_min, k_max + 1):
        groups = [[] for _ in range(keylen)]
        for i, l in enumerate(letters):
            groups[i % keylen].append(l)

        avg_ic = sum(calculate_ic(col) for col in groups) / keylen

        print(keylen, avg_ic)  # debug visual

        if avg_ic > best_ic:
            best_ic = avg_ic
            best_keylen = keylen

    return best_keylen


def analyze_group_shift(group, alphabet_freq):
    """
    Calcula a correlação de frequências (Índice de Coincidência Mútuo) para os 26 deslocamentos.
    """
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
    cipher_text = "Nfwer hpnnb hivf zou vq, newfr gpona mft ypv doxo, newfr gpona svn aspune bnd efsesu yov. Oevfs goooa mble ypv crz, oevfs goooa sbz gopebyf, oevfs goooa tfml a mje aoe husu yov."
    real_key = "ABBA"

    print(" [ETAPA 1] Estimando tamanho da chave via IC ")
    keylen = find_key_length(cipher_text, 2, 7)
    print(f"\n=> Tamanho de chave mais provável: {keylen}\n")

    key_found = reconstruct_key(cipher_text, keylen, FREQ_EN)
    print("\nchave reconstruída:", key_found)
    print("chave real:         ", real_key)

    plaintext = decrypt(cipher_text, key_found)
    print(f"\ntexto decifrado: {plaintext}")


if __name__ == "__main__":
    main()