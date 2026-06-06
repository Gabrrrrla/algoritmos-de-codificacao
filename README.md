# Algoritmos de Codificação, Detecção e Correção de Erros

Implementação em Python de algoritmos clássicos de codificação e tratamento de erros: **Golomb**, **Elias-Gamma**, **Fibonacci/Zeckendorf**, **Huffman**, **CRC-4**, **Hamming (7,4)** e **Código de Repetição**. Feito por Ana Beatriz Stahl, Emanuele Schlemmer Thomazzoni, Gabriela Bley Rodrigues e Luisa Becker dos Santos.

## Descrição

Este projeto fornece implementações completas e testadas de algoritmos de codificação e tratamento de erros, com **interface gráfica (GUI)**, **linha de comando (CLI)** e **comunicação cliente/servidor via socket** que permitem:

- Codificar dados usando diferentes algoritmos
- Decodificar strings binárias de volta aos dados originais
- Inserir erros manualmente ou automaticamente nos codewords
- Detectar erros utilizando CRC-4
- Corrigir erros utilizando Hamming (7,4) e Código de Repetição
- Transmitir codewords entre cliente e servidor via socket UDP
- Visualizar resultados e estatísticas de compressão

### Interfaces Disponíveis

1. **GUI (Graphical User Interface)** - Interface gráfica com tkinter
   - Ideal para iniciantes e uso interativo
   - Visualização clara de resultados
   - Abas separadas para codificação e decodificação

2. **CLI (Command Line Interface)** - Interface de terminal
   - Menu interativo no terminal

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
# Clone o repositório
git clone https://github.com/stahlbia/algoritmos-de-codificacao.git
cd algoritmos-de-codificacao

# Opcional - Criar um ambiente virtual para o python
python -m venv .venv

# Opcional - Ativar o ambiente virtual
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Ou instale em modo desenvolvimento
pip install -e .
```

## Uso

### Interface Gráfica (GUI)

Execute a interface gráfica:

```bash
python -m run_gui
```

#### Demonstração da interface gráfica

##### 1. Tela inicial da aplicação

![Tela inicial da GUI](docs/images/gui_main.png)

Visão geral da interface, com seleção de algoritmo, entrada de dados e área de resultado.

##### 2. Exemplo de codificação com Golomb

![Exemplo com Golomb](docs/images/gui_golomb_e.png)

Uso do parâmetro `m` e codificação de uma sequência de números inteiros não negativos.

##### 3. Exemplo de decodificação com Golomb

![Exemplo com Golomb](docs/images/gui_golomb_d.png)

Uso do parâmetro `m` e decodificação de uma sequência de números inteiros não negativos.

##### 4. Exemplo de codificação com Elias-Gamma

![Exemplo com Elias-Gamma](docs/images/gui_eliasgamma_e.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

##### 5. Exemplo de decodificação com Elias-Gamma

![Exemplo com Elias-Gamma](docs/images/gui_eliasgamma_d.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

##### 6. Exemplo de codificação com Fibonacci

![Exemplo com Golomb](docs/images/gui_fibonacci_e.png)

Uso do parâmetro `m` e codificação de uma sequência de números inteiros não negativos.

##### 7. Exemplo de decodificação com Fibonacci

![Exemplo com Golomb](docs/images/gui_fibonacci_d.png)

Uso do parâmetro `m` e decodificação de uma sequência de números inteiros não negativos.

##### 8. Exemplo de codificação com Huffman

![Exemplo com Huffman](docs/images/gui_huffman_e.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

##### 9. Exemplo de decodificação com Huffman

![Exemplo com Huffman](docs/images/gui_huffman_d.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

##### 10. Exemplo de codificação com Código de Repetição

![Exemplo com Código de Repetição](docs/images/gui_repetition_e.png)

Codificação de codeword binário com repetição de bits e quantidade de repetições configurável.

##### 11. Exemplo de decodificação com Código de Repetição

![Exemplo com Código de Repetição](docs/images/gui_repetition_d.png)

Decodificação por votação majoritária e exibição do resultado corrigido.

##### 12. Exemplo de uso do CRC-4

![Exemplo com CRC-4](docs/images/gui_crc_e.png)

Geração dos bits redundantes, anexo ao codeword e verificação de integridade na recepção.

##### 13. Exemplo de codificação com Hamming (7,4)

![Exemplo com Hamming](docs/images/gui_hamming_e.png)

Codificação de bloco de 4 bits com adição dos bits de paridade.

##### 14. Exemplo de decodificação com Hamming (7,4)

![Exemplo com Hamming](docs/images/gui_hamming_d.png)

Decodificação com detecção e correção de erro de 1 bit, exibindo posição do erro e mensagem corrigida.

---

### Interface de Linha de Comando (CLI)

Execute a interface de terminal:

```bash
python -m run_cli
```

#### Menu Interativo

A CLI apresenta um menu onde você pode:

1. Selecionar o algoritmo de codificação
2. Escolher entre codificar ou decodificar
3. Inserir dados e visualizar resultados

### Comunicação Cliente/Servidor (Socket)

O sistema implementa comunicação via socket UDP. O fluxo é:

1. O **cliente** codifica a mensagem e opcionalmente insere erros nos bits
2. O **cliente** envia o codeword ao servidor via socket
3. O **servidor** recebe o codeword, verifica e corrige erros (CRC, Hamming, Repetição)
4. O **servidor** retorna ao cliente o resultado da verificação e o codeword corrigido

Inicie o servidor em um terminal:

```bash
python run_server.py
```

Em outro terminal, inicie o cliente:

```bash
python -m run_cli
```

Cliente e servidor podem executar na mesma máquina utilizando `localhost` (`127.0.0.1`).

### Exemplos de Uso Programático

#### Golomb

```python
from src.algorithms.golomb import encode, decode

result = encode([0, 5, 10, 15], m=4)
print(f"Codificado: {result.encoded}")

decoded = decode(result.encoded, m=4)
print(f"Decodificado: {decoded.numbers}")
```

#### Elias-Gamma

```python
from src.algorithms.elias_gamma import encode, decode

result = encode([1, 5, 10, 17])
print(f"Codificado: {result.encoded}")

decoded = decode(result.encoded)
print(f"Decodificado: {decoded.numbers}")
```

#### Fibonacci/Zeckendorf

```python
from src.algorithms.fibonacci import encode, decode

result = encode([1, 3, 7, 15])
print(f"Codificado: {result.encoded}")

decoded = decode(result.encoded)
print(f"Decodificado: {decoded.numbers}")
```

#### Huffman

```python
from src.algorithms.huffman import encode, decode

result = encode("hello world")
print(f"Codificado: {result.encoded}")
print(f"Tabela de códigos: {result.code_table}")

decoded = decode(result.encoded, result.code_table)
print(f"Decodificado: {decoded.text}")
```

#### CRC-4

```python
from src.algorithms.crc import encode, verify

result = encode("1011")
print(f"Codeword com CRC: {result.encoded}")

check = verify(result.encoded)
print(f"Erro detectado: {check.has_error}")
```

#### Hamming (7,4)

```python
from src.algorithms.hamming import encode, decode

result = encode("1011")
print(f"Codificado: {result.encoded}")

decoded = decode(result.encoded)
print(f"Decodificado: {decoded.decoded}")
print(f"Posição do erro: {decoded.error_position}")
```

#### Código de Repetição

```python
from src.algorithms.repetition import encode, decode

result = encode("101", repetitions=3)
print(f"Codificado: {result.encoded}")

decoded = decode(result.encoded, repetitions=3)
print(f"Decodificado: {decoded.decoded}")
```

## Algoritmos Implementados

### Algoritmos de Compressão e Codificação

#### 1. Golomb

**Descrição**: Algoritmo de compressão com parâmetro ajustável `m`. Indicado para codificação de inteiros não negativos, especialmente em cenários em que os dados seguem distribuição geométrica.

**Características**:

- Parâmetro `m` ajustável
- Codifica números não-negativos
- Divide números em quociente (unário) e resto (binário)
- Entrada esperada de inteiros > 0

**Complexidade**: O(n) onde n é o valor a codificar

#### 2. Elias-Gamma

**Descrição**: Código universal para inteiros positivos. Não requer parâmetros.

**Características**:

- Auto-delimitante
- Eficiente para números pequenos
- Codifica comprimento em unário + valor em binário

**Complexidade**: O(log n)

#### 3. Fibonacci/Zeckendorf

**Descrição**: Baseado na representação de Zeckendorf usando números de Fibonacci não-consecutivos.

**Características**:

- Usa terminador `11`
- Representação única para cada número
- Baseado em números de Fibonacci

**Complexidade**: O(log n)

#### 4. Huffman

**Descrição**: Algoritmo de compressão baseado em frequência de símbolos. A árvore é construída com base na frequência dos símbolos informados antes da codificação.

**Características**:

- Código de comprimento variável
- Ótimo para compressão baseada em frequência
- Constrói árvore binária
- Símbolos mais frequentes têm códigos mais curtos

**Complexidade**: O(n log n) para construção da árvore

### Algoritmos de Detecção e Correção de Erros

#### 5. CRC-4

**Descrição**: Detecção de erros por Cyclic Redundancy Check. Utiliza obrigatoriamente o polinômio gerador `G(x) = x^4 + x + 1` (representação binária: `10011`).

**Características**:

- Gera bits redundantes e os anexa ao codeword
- Verifica erros na recepção
- Informa se houve erro na transmissão
- Entrada: codeword binário válido

#### 6. Hamming (7,4)

**Descrição**: Código de correção de erros que adiciona 3 bits de paridade a blocos de 4 bits de dados, permitindo detectar e corrigir erros de 1 bit.

**Características**:

- Blocos de 4 bits de dados → 7 bits codificados
- Detecta e corrige erros de 1 bit
- Informa a posição do erro

#### 7. Código de Repetição (Ri)

**Descrição**: Correção de erros por repetição de bits. Cada bit é repetido `i` vezes e o valor correto é determinado por votação majoritária.

**Características**:

- Quantidade de repetições configurável
- Correção por maioria de votos
- Adequado para canais com baixa taxa de erro

## Estrutura do Projeto

```txt
algoritmos-de-codificacao/
├── docs/
│   └── images/                        # Imagens das interfaces
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── crc.py                     # CRC-4
│   │   ├── elias_gamma.py             # Elias-Gamma
│   │   ├── fibonacci.py               # Fibonacci/Zeckendorf
│   │   ├── golomb.py                  # Golomb
│   │   ├── hamming.py                 # Hamming (7,4)
│   │   ├── huffman.py                 # Huffman
│   │   └── repetition.py              # Código de Repetição
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── gui.py                     # Interface gráfica
│   │   └── cli.py                     # Interface de linha de comando
│   ├── network/
│   │   ├── __init__.py
│   │   ├── client.py                  # Cliente UDP
│   │   ├── protocol.py                # Protocolo de comunicação
│   │   └── server.py                  # Servidor UDP
│   └── utils/
│       ├── __init__.py
│       ├── huffman_input_parser.py    # Parser de entrada Huffman
│       ├── input_parser.py            # Parser de entrada geral
│       └── validation.py              # Validação de entrada
├── tests/
│   ├── __init__.py
│   ├── test_crc.py
│   ├── test_elias_gamma.py
│   ├── test_fibonacci.py
│   ├── test_golomb.py
│   ├── test_hamming.py
│   ├── test_huffman.py
│   └── test_repetition_code.py
├── requirements.txt
├── run_cli.py
├── run_gui.py
├── run_server.py
├── .gitignore
└── README.md
```

## Testes

Execute os testes usando pytest:

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_huffman.py
```

## Comparação de Algoritmos

### Compressão e Codificação

| Algoritmo       | Tipo        | Entrada        | Parâmetros | Melhor Para                    |
| --------------- | ----------- | -------------- | ---------- | ------------------------------ |
| **Golomb**      | Paramétrico | Não-negativos  | m          | Distribuições geométricas      |
| **Elias-Gamma** | Universal   | Positivos      | Nenhum     | Números pequenos               |
| **Fibonacci**   | Universal   | Positivos      | Nenhum     | Representação única            |
| **Huffman**     | Estatístico | Texto/símbolos | Nenhum     | Dados com frequências variadas |

### Detecção e Correção de Erros

| Algoritmo          | Tipo     | Entrada          | Parâmetros     | Capacidade                      |
| ------------------ | -------- | ---------------- | -------------- | ------------------------------- |
| **CRC-4**          | Detecção | Binário          | Nenhum         | Detecta erros, não corrige      |
| **Hamming (7,4)**  | Correção | Binário (4 bits) | Nenhum         | Corrige 1 bit por bloco         |
| **Repetição (Ri)** | Correção | Binário          | i (repetições) | Corrige por votação majoritária |

## Referências

- **Golomb Coding**: Solomon W. Golomb (1966)
- **Elias Coding**: Peter Elias (1975)
- **Zeckendorf's Theorem**: Edouard Zeckendorf (1972)
- **Huffman Coding**: David A. Huffman (1952)
- **Hamming Codes**: Richard W. Hamming (1950)
- **CRC**: W. Wesley Peterson & D. T. Brown (1961)
