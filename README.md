# Cifra de Vigenère + Criptoanálise

Projeto dividido em dois módulos independentes:

- **`vigenere/`** — cifra e decifra texto usando Vigenère (chave conhecida).
- **`break_the_rules/`** — tenta quebrar a cifra sem conhecer a chave, estimando o tamanho dela (Kasiski + Índice de Coincidência) e reconstruindo-a por análise de frequência.



Todos os comandos abaixo devem ser executados **a partir da raiz do projeto**, usando `-m` (não rode os arquivos `.py` diretamente com caminho, ou os imports entre pacotes vão quebrar).

## `vigenere` — cifrar e decifrar

```bash
python -m vigenere.main -op encrypt -t "texto secreto" -k CHAVE
python -m vigenere.main -op decrypt -t "texto cifrado" -k CHAVE
```

Se `-k` não for informado, uma chave é gerada automaticamente (`keygen`).

**Arquivos .txt**:

```bash
python -m vigenere.main -op encrypt -f textos/entrada.txt -k CHAVE
```

O resultado vai para `outputs/output_encrypt.txt` (ou `output_decrypt.txt`).

**Rodar um caso de teste pré-definido**:

```bash
python -m vigenere.main -op encrypt --test 0
```

## `break_the_rules` — quebrar a cifra sem saber a chave

```bash
python -m break_the_rules.main -t "texto cifrado" -lang ptbr
python -m break_the_rules.main -t "ciphertext" -lang en
```

`-lang` aceita `ptbr` ou `en` (frequências de referência em `frequencies.py`).

**Arquivo .txt**:

```bash
python -m break_the_rules.main -f textos/cifrado.txt -lang ptbr
```

O texto decifrado é escrito em `<nome_do_arquivo>_decrypted<extensão>`, ao lado do arquivo de entrada.

**Comparar com a chave real** (só para conferência, não é usada na quebra):

```bash
python -m break_the_rules.main -t "texto cifrado" -lang ptbr -k CHAVEREAL
```

**Rodar um caso de teste pré-definido:**

```bash
python -m break_the_rules.main --test 0
```
