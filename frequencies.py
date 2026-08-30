"""
Frequências de letras em português e inglês, usadas como referência na análise de frequência.
Fonte de referência: https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras
"""


FREQ_PT = {
    "a": 0.1463,
    "b": 0.0104,
    "c": 0.0388,
    "d": 0.0499,
    "e": 0.1257,
    "f": 0.0102,
    "g": 0.0130,
    "h": 0.0128,
    "i": 0.0618,
    "j": 0.0040,
    "k": 0.0002,
    "l": 0.0278,
    "m": 0.0474,
    "n": 0.0505,
    "o": 0.1073,
    "p": 0.0252,
    "q": 0.0120,
    "r": 0.0653,
    "s": 0.0781,
    "t": 0.0434,
    "u": 0.0463,
    "v": 0.0167,
    "w": 0.0001,
    "x": 0.0021,
    "y": 0.0001,
    "z": 0.0047,
}

FREQ_EN = {
    "a": 0.0817,
    "b": 0.0129,
    "c": 0.0278,
    "d": 0.0425,
    "e": 0.1270,
    "f": 0.0223,
    "g": 0.0202,
    "h": 0.0609,
    "i": 0.0697,
    "j": 0.0015,
    "k": 0.0077,
    "l": 0.0403,
    "m": 0.0241,
    "n": 0.0675,
    "o": 0.0751,
    "p": 0.0193,
    "q": 0.0010,
    "r": 0.0599,
    "s": 0.0633,
    "t": 0.0906,
    "u": 0.0276,
    "v": 0.0098,
    "w": 0.0236,
    "x": 0.0015,
    "y": 0.0197,
    "z": 0.0007,
}


# Índice de coincidência esperado para texto corrido em cada língua
IC_PT = sum(f**2 for f in FREQ_PT.values())  # ~0.0781
IC_EN = sum(f**2 for f in FREQ_EN.values())  # ~0.0667
IC_RANDOM = 1 / 26  # ~0.0385


