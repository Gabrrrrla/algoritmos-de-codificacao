# Algoritmos de Codificação

Implementação em Python de algoritmos clássicos de codificação: **Golomb**, **Elias-Gamma**, **Fibonacci/Zeckendorf** e **Huffman**. Feito por Ana Beatriz Stahl, Emanuele Schlemmer Thomazzoni, Gabriela Bley Rodrigues e Luisa Becker dos Santos.

## 📋 Descrição

Este projeto fornece implementações completas e testadas de algoritmos de codificação, com **interface gráfica (GUI)** e **linha de comando (CLI)** que permitem:

- ✅ **Interface Gráfica Intuitiva** - Use com cliques, sem comandos
- ✅ Codificar dados usando diferentes algoritmos
- ✅ Decodificar strings binárias de volta aos dados originais
- ✅ Visualizar resultados e estatísticas de compressão
- ✅ Copiar resultados facilmente

### 🎨 Interfaces Disponíveis

1. **GUI (Graphical User Interface)** - Interface gráfica com tkinter
   - Ideal para iniciantes e uso interativo
   - Visualização clara de resultados
   - Abas separadas para codificação e decodificação

2. **CLI (Command Line Interface)** - Interface de terminal
   - Menu interativo no terminal

## 🚀 Instalação

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

## 💻 Uso

### Interface Gráfica (GUI)

Execute a interface gráfica:

```bash
python -m run_gui
```

## Demonstração da interface gráfica

### 1. Tela inicial da aplicação

![Tela inicial da GUI](docs/images/gui_main.png)

Visão geral da interface, com seleção de algoritmo, entrada de dados e área de resultado.

### 2. Exemplo de codificação com Golomb

![Exemplo com Golomb](docs/images/gui_golomb_e.png)

Uso do parâmetro `m` e codificação de uma sequência de números inteiros não negativos.

### 3. Exemplo de decodificação com Golomb

![Exemplo com Golomb](docs/images/gui_golomb_d.png)

Uso do parâmetro `m` e decodificação de uma sequência de números inteiros não negativos.

### 4. Exemplo de codificação com Elias-Gamma

![Exemplo com Elias-Gamma](docs/images/gui_eliasgamma_e.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

### 5. Exemplo de decodificação com Elias-Gamma

![Exemplo com Elias-Gamma](docs/images/gui_eliasgamma_d.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

### 6. Exemplo de codificação com Fibonacci

![Exemplo com Golomb](docs/images/gui_fibonacci_e.png)

Uso do parâmetro `m` e codificação de uma sequência de números inteiros não negativos.

### 7. Exemplo de decodificação com Fibonacci

![Exemplo com Golomb](docs/images/gui_fibonacci_d.png)

Uso do parâmetro `m` e decodificação de uma sequência de números inteiros não negativos.

### 8. Exemplo de codificação com Huffman

![Exemplo com Huffman](docs/images/gui_huffman_e.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

### 9. Exemplo de decodificação com Huffman

![Exemplo com Huffman](docs/images/gui_huffman_d.png)

Codificação de texto, tabela de códigos gerada e análise visual do resultado.

---

### Interface de Linha de Comando (CLI)

Execute a interface de terminal:

```bash
python -m run_cli
```

### Menu Interativo

A CLI apresenta um menu onde você pode:

1. Selecionar o algoritmo de codificação
2. Escolher entre codificar ou decodificar
3. Inserir dados e visualizar resultados

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

## 📚 Algoritmos Implementados

### 1. Golomb

**Descrição**: Algoritmo de compressão com parâmetro ajustável `m`. Indicado para codificação de inteiros não negativos, especialmente em cenários em que os dados seguem distribuição geométrica.

**Características**:

- Parâmetro `m` ajustável
- Codifica números não-negativos
- Divide números em quociente (unário) e resto (binário)
- Entrada esperada de inteiros > 0

**Complexidade**: O(n) onde n é o valor a codificar

### 2. Elias-Gamma

**Descrição**: Código universal para inteiros positivos. Não requer parâmetros.

**Características**:

- Auto-delimitante
- Eficiente para números pequenos
- Codifica comprimento em unário + valor em binário

**Complexidade**: O(log n)

### 3. Fibonacci/Zeckendorf

**Descrição**: Baseado na representação de Zeckendorf usando números de Fibonacci não-consecutivos.

**Características**:

- Usa terminador '11'
- Representação única para cada número
- Baseado em números de Fibonacci

**Complexidade**: O(log n)

### 4. Huffman

**Descrição**: Algoritmo de compressão baseado em frequência de símbolos.

**Características**:

- Código de comprimento variável
- Ótimo para compressão baseada em frequência
- Constrói árvore binária
- Símbolos mais frequentes têm códigos mais curtos

**Complexidade**: O(n log n) para construção da árvore

## 🗂️ Estrutura do Projeto

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
│       ├── binary_utils.py            # Utilitários para binário
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

## 🧪 Testes

Execute os testes usando pytest:

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_huffman.py
```

## 📊 Comparação de Algoritmos

| Algoritmo | Tipo | Entrada | Parâmetros | Melhor Para |
| --------- | ---- | ------- | ---------- | ----------- |
| **Golomb** | Paramétrico | Não-negativos | m | Distribuições geométricas |
| **Elias-Gamma** | Universal | Positivos | Nenhum | Números pequenos |
| **Fibonacci** | Universal | Positivos | Nenhum | Representação única |
| **Huffman** | Estatístico | Texto/símbolos | Nenhum | Dados com frequências variadas |

## 🔗 Referências

- **Golomb Coding**: Solomon W. Golomb (1966)
- **Elias Coding**: Peter Elias (1975)
- **Zeckendorf's Theorem**: Edouard Zeckendorf (1972)
- **Huffman Coding**: David A. Huffman (1952)
