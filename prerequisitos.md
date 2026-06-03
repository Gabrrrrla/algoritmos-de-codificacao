# Trabalho Prático 2 - Codificação de Canal e Tratamento de Erro

**Atividade Acadêmica:** Teoria da Informação: Compressão e Criptografia

**Professor:** Elvandi da Silva Júnior

**Modalidade:** Individual ou em grupo de até 4 alunos | **Peso:** 40

---

O Trabalho Prático 2 consiste na continuação e evolução do Trabalho Prático 1.

O sistema desenvolvido no Trabalho Prático 1 deverá ser reutilizado e expandido, mantendo todas as funcionalidades anteriormente implementadas e adicionando os algoritmos de detecção e correção de erro solicitados neste trabalho.

O objetivo é criar um sistema completo de codificação, compressão, detecção e correção de erro, permitindo ao usuário:

- inserir símbolos, palavras, frases ou codewords binários;
- realizar codificação e decodificação;
- inserir erros manualmente;
- transmitir os dados entre cliente e servidor utilizando sockets;
- verificar e corrigir erros utilizando diferentes algoritmos.

A linguagem de programação é de livre escolha.

## Requisitos Obrigatórios

O Trabalho Prático 2 deverá obrigatoriamente manter todas as funcionalidades implementadas no Trabalho Prático 1, incluindo:

- Golomb;
- Elias-Gamma;
- Fibonacci/Zeckendorf;
- Huffman;
- codificação;
- decodificação;
- validação de entrada;
- suporte a múltiplos símbolos;
- inserção de erro.

Além disso, deverão ser adicionadas as funcionalidades descritas neste Trabalho Prático 2.

## Requisitos Funcionais

### 1. Entrada de Dados

O sistema deve permitir ao usuário inserir:

- números inteiros positivos;
- símbolos textuais;
- palavras completas;
- frases simples;
- codewords binários.

O sistema deverá aceitar entrada contendo um e/ou múltiplos símbolos.

Entradas múltiplas poderão ser informadas:

- separadas por espaço;
- separadas por vírgula;
- como texto contínuo.

Quando algoritmos baseados em inteiros forem utilizados, símbolos textuais deverão ser convertidos automaticamente para ASCII ou Unicode.

### 2. Métodos de Compressão e Codificação

O sistema deverá manter os algoritmos implementados no Trabalho Prático 1:

- Golomb;
- Elias-Gamma;
- Fibonacci/Zeckendorf;
- Huffman.

### 3. Métodos de Tratamento de Erro

O sistema deverá adicionar os seguintes algoritmos:

#### Correção de erro

- Código de repetição Ri;
- Hamming (7,4).

#### Detecção de erro

- CRC (Cyclic Redundancy Check).

### 4. CRC (Obrigatório)

Para padronização da atividade, o algoritmo CRC deverá utilizar obrigatoriamente o seguinte polinômio gerador:

CRC-4 utilizando o polinômio gerador:

```txt
G(x) = x^4 + x + 1
```

Representação binária: `10011`

O sistema deverá:

- gerar os bits redundantes do CRC;
- anexar o CRC ao codeword;
- verificar erros na recepção;
- informar se houve erro ou não na transmissão.

### 5. Codificação

O sistema deve ser capaz de codificar os símbolos inseridos com base no método selecionado pelo usuário.

Para Huffman, o sistema deverá construir automaticamente a árvore de codificação com base na frequência dos símbolos informados.

### 6. Inserção de Erro

O sistema deverá permitir:

- inserção manual de erro em bits;
- inserção automática de erro;
- alteração de um ou mais bits do codeword.

O objetivo é demonstrar o funcionamento dos algoritmos de detecção e correção de erro.

### 7. Decodificação e Verificação

O sistema deverá:

- decodificar mensagens utilizando:
  - Golomb;
  - Elias-Gamma;
  - Fibonacci/Zeckendorf;
  - Huffman;
  - Código de repetição Ri (repetição de bits);
  - Hamming (7,4);
- verificar integridade utilizando CRC;
- informar:
  - mensagem recebida;
  - presença de erro;
  - posição do erro (quando aplicável);
  - mensagem corrigida (quando possível).

### 8. Comunicação Cliente/Servidor (Socket)

O sistema deverá implementar comunicação utilizando sockets.

#### Cliente

O cliente deverá:

- codificar a mensagem;
- enviar o codeword ao servidor.

#### Servidor

O servidor deverá:

- receber o codeword;
- verificar ou corrigir os erros;
- retornar o resultado ao cliente.

A implementação pode utilizar TCP ou UDP.

Cliente e servidor deverão executar simultaneamente em processos separados.

Devido às limitações de segurança e comunicação do laboratório, será permitido executar cliente e servidor na mesma máquina utilizando localhost (127.0.0.1).

### 9. Validação de Entrada

O sistema deverá validar todas as entradas do usuário, garantindo compatibilidade com os algoritmos implementados.

Exemplos:

- Elias-Gamma: somente inteiros positivos não nulos;
- Hamming: tamanho correto dos blocos;
- CRC: entrada binária válida;
- Repetição: quantidade válida de repetições.

### 10. Exibição do Resultado

O sistema deverá exibir claramente:

- dados de entrada;
- dados convertidos para ASCII/Unicode;
- codeword gerado;
- bits redundantes;
- erro inserido;
- resultado da verificação;
- mensagem corrigida;
- mensagem decodificada.

## Critérios de Avaliação

| Critério                       | Peso   |
| ------------------------------ | ------ |
| Interface e usabilidade        | 4      |
| Codificação correta            | 6      |
| Decodificação correta          | 6      |
| Implementação correta do CRC   | 4      |
| Inserção e tratamento de erros | 4      |
| Comunicação via socket         | 6      |
| Validação de entrada           | 4      |
| Suporte a múltiplos símbolos   | 3      |
| Organização e documentação     | 3      |
| **Total**                      | **40** |

## Observações

1. O Trabalho Prático 2 é continuação obrigatória do Trabalho Prático 1.
2. Todas as funcionalidades do Trabalho Prático 1 deverão permanecer funcionais.
3. Trabalhos que implementarem apenas os algoritmos novos, sem manter os anteriores, serão considerados incompletos.
4. Os algoritmos deverão funcionar para entradas arbitrárias fornecidas pelo usuário, não sendo aceitas implementações limitadas a exemplos fixos previamente definidos no código.
5. O sistema deve permitir entrada contendo múltiplos símbolos.
6. Entradas textuais deverão ser convertidas automaticamente para ASCII ou Unicode quando necessário.
7. Trabalhos que aceitarem apenas números nos algoritmos baseados em inteiros serão considerados parcialmente corretos.
8. A interface pode ser textual (console) ou gráfica.
9. O trabalho deverá ser apresentado em funcionamento durante a avaliação.
10. O sistema deverá possuir codificação e decodificação funcional para todos os algoritmos solicitados.
11. O código deverá ser de autoria dos alunos. Trabalhos com indícios de cópia ou utilização indevida de ferramentas automáticas poderão ser desconsiderados.
12. Durante a apresentação, poderá ser solicitado teste com entradas definidas pelo professor.

## Dúvidas de Interpretação

### O Huffman exigido é o adaptativo?

Não. O documento menciona Huffman apenas como algoritmo herdado do Trabalho Prático 1, sem especificar variante adaptativa. A seção 5 descreve o Huffman clássico (estático), onde a árvore é construída com base na frequência dos símbolos informados antes da codificação.

### A inserção de erro é uma etapa separada entre encode e decode?

Sim. A inserção de erro não ocorre durante a codificação nem durante a decodificação — ela é uma etapa intermediária que simula ruído no canal de transmissão. O fluxo é:

1. **Encode** → gera o codeword
2. **Inserção de erro** → modifica bits do codeword manualmente ou automaticamente
3. **Transmissão via socket** → envia o codeword corrompido
4. **Decode/Verificação** → detecta e/ou corrige o erro, informando posição e mensagem corrigida

### No fluxo de sockets, o servidor apenas verifica e corrige, devolvendo o resultado ao cliente?

Sim. O fluxo é:

1. **Cliente** → usuário insere a mensagem e codifica (Golomb, Huffman, etc.)
2. **Cliente** → opcionalmente insere erro manual nos bits
3. **Cliente** → envia o codeword ao servidor via socket
4. **Servidor** → recebe o codeword, verifica e corrige erros (CRC, Hamming, Repetição)
5. **Servidor** → retorna ao cliente o resultado da verificação e o codeword corrigido (se houver erro)
6. **Cliente** → exibe o resultado recebido

O servidor atua como receptor do canal — não conhece a mensagem original, apenas recebe o codeword (possivelmente corrompido) e aplica os algoritmos de detecção e correção.

### CRC, Hamming e código de repetição devem estar disponíveis também fora do fluxo socket, apenas no cliente?

O documento não exige isso. Esses algoritmos são descritos exclusivamente no contexto do fluxo de transmissão via socket, onde o objetivo é simular um canal com ruído. A verificação e correção são responsabilidade do servidor. Uma opção standalone no cliente não é proibida, mas também não é requisito avaliado.
