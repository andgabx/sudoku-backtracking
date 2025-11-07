# 🧩 Análise de Complexidade: Backtracking Iterativo para Sudoku

**Projeto de Teoria da Computação**  
**Prof. Daniel Bezerra - CESAR School**  
**Outubro/Novembro 2025**

---

## 📋 Descrição do Projeto

Este projeto implementa e analisa a complexidade de tempo do algoritmo de **Backtracking Iterativo** para resolver puzzles de Sudoku. O objetivo é realizar uma análise comparativa detalhada considerando:

- **Duas linguagens de programação**: C e Python
- **Três tamanhos de problema**: Small (3×3), Medium (6×6), Large (9×9)
- **Dois casos de teste**: Melhor caso e Pior caso
- **30 execuções** para cada combinação de parâmetros
- **Medição de tempo** e **contagem de iterações**

### 🎯 Características Principais

✅ **Backtracking Iterativo** (não recursivo) usando estruturas de dados explícitas:
   - **C**: Pilha (`Stack`) implementada com array dinâmico
   - **Python**: Lista usada como pilha

✅ **Gerador de Puzzles Válidos** com configurações controladas de dificuldade

✅ **Sistema de Logging** completo salvando resultados em arquivos

✅ **Makefile robusto** com automação completa de todos os testes

---

## 🏗️ Arquitetura do Projeto

```
sudoku_backtracking/
│
├── c/                          # Implementação em C
│   ├── include/                # Headers (.h)
│   │   ├── sudoku.h           # Estrutura e operações do Sudoku
│   │   ├── backtracking.h     # Algoritmo de backtracking iterativo
│   │   └── generator.h        # Gerador de puzzles válidos
│   │
│   └── src/                    # Código fonte (.c)
│       ├── sudoku.c           # Implementação das operações
│       ├── backtracking.c     # Implementação do backtracking
│       ├── generator.c        # Implementação do gerador
│       └── main.c             # Programa principal
│
├── python/                     # Implementação em Python
│   └── src/                    # Módulos Python
│       ├── sudoku.py          # Classe Sudoku
│       ├── backtracking.py    # Algoritmo de backtracking iterativo
│       ├── generator.py       # Gerador de puzzles
│       └── main.py            # Programa principal
│
├── logs/                       # Logs gerados (criado automaticamente)
│   ├── c_small_best.log
│   ├── c_small_worst.log
│   ├── python_small_best.log
│   └── ... (12 arquivos no total)
│
├── analyze_results.py          # Script de análise e visualização de resultados
├── Makefile                    # Automação de compilação e testes
└── README.md                   # Este arquivo
```

---

## 🚀 Como Usar

### Pré-requisitos

- **GCC** (compilador C)
- **Python 3.x**
- **Make**

### Compilação

```bash
# Compila o código C
make build
```

### Execução de Testes Individuais

```bash
# Sintaxe geral
make run SIZE=<tamanho> CASE=<caso> LANG=<linguagem>

# Exemplos
make run SIZE=small CASE=best LANG=c
make run SIZE=large CASE=worst LANG=python
make run SIZE=medium CASE=best LANG=c
```

**Parâmetros:**
- `SIZE`: `small`, `medium`, `large`
- `CASE`: `best`, `worst`
- `LANG`: `c`, `python`

### Execução Completa (Todas as Combinações)

```bash
# Executa TODAS as 12 combinações (360 testes no total)
make run-all
```

Este comando:
- Compila o código C automaticamente
- Executa 3 sizes × 2 cases × 2 linguagens = 12 combinações
- Cada combinação executa 30 testes
- Gera 12 arquivos de log com resultados completos

**⏱️ Tempo estimado**: 5-15 minutos (dependendo do hardware)

### Teste Rápido

```bash
# Teste rápido para validar o funcionamento
make test
```

### Limpeza

```bash
# Remove arquivos compilados e logs
make clean
```

### Análise de Resultados

```bash
# Analisa os logs e gera relatório comparativo
python3 analyze_results.py
```

Este script:
- Extrai estatísticas de todos os arquivos de log
- Gera tabelas comparativas entre C e Python
- Calcula speedup entre as linguagens
- Analisa melhor caso vs pior caso
- Útil para criação de gráficos no relatório

### Ajuda

```bash
# Exibe menu de ajuda completo
make help
```

---

## 📊 Configuração dos Casos de Teste

| Tamanho | Dimensão | Melhor Caso (vazias) | Pior Caso (vazias) |
|---------|----------|----------------------|--------------------|
| Small   | 3×3      | 2-3                  | 5-6                |
| Medium  | 6×6      | 8-10                 | 20-24              |
| Large   | 9×9      | 20-25                | 50-60              |

**Melhor Caso**: Puzzles com poucas células vazias, mais fáceis de resolver  
**Pior Caso**: Puzzles com muitas células vazias, mais difíceis de resolver

---

## 📝 Formato dos Logs

Cada arquivo de log contém:

```
=== Análise de Complexidade - Backtracking Iterativo para Sudoku ===
Linguagem: C / Python
Tamanho: NxN
Caso: best / worst
Células vazias alvo: X
Número de execuções: 30

Execução 1:
  Células vazias: X
  Tempo: 0.XXXXXX segundos
  Iterações: XXXX
  Resolvido: Sim

[... 30 execuções ...]

=== ESTATÍSTICAS FINAIS ===
Resoluções bem-sucedidas: 30/30
Tempo médio: 0.XXXXXX segundos
Tempo total: 0.XXXXXX segundos
Iterações médias: XXX.XX
Iterações totais: XXXXX
```

---

## 🧠 Detalhes da Implementação

### Backtracking Iterativo

Ao contrário da implementação recursiva tradicional, este projeto usa **backtracking iterativo** com pilha explícita:

#### C - Stack
```c
typedef struct {
    State* items;
    int top;
    int capacity;
} Stack;
```

Operações: `stack_push()`, `stack_pop()`, `stack_is_empty()`

#### Python - Lista
```python
stack = []  # Lista usada como pilha
stack.append(state)  # Push
state = stack.pop()  # Pop
```

### Fluxo do Algoritmo

1. **Inicialização**: Encontra primeira célula vazia e empilha estado inicial
2. **Loop Principal**: Enquanto a pilha não estiver vazia:
   - Desempilha estado atual
   - Tenta números de 1 a N
   - Se encontrar número válido:
     - Coloca na célula
     - Empilha estado para backtrack
     - Encontra próxima célula vazia
     - Se não houver mais vazias → **Resolvido!**
   - Se não encontrar número válido → **Backtrack** (continua loop)
3. **Fim**: Sudoku resolvido ou pilha vazia (impossível resolver)

### Vantagens da Implementação Iterativa

✅ **Controle explícito** do estado do algoritmo  
✅ **Sem limite de recursão** (evita stack overflow)  
✅ **Contagem precisa** de iterações  
✅ **Mais eficiente** em algumas linguagens (menos overhead)

---

## 📈 Análise de Complexidade

### Classificação Assintótica

- **Pior Caso**: O(N^M) onde:
  - N = tamanho do Sudoku (3, 6, 9)
  - M = número de células vazias

- **Melhor Caso**: O(M) onde M é o número de células vazias (quando não há backtracking necessário)

- **Caso Médio**: O(N^(M/2)) aproximadamente, dependendo da configuração do puzzle

### Classes de Complexidade

- **Classe P?**: Não, o problema geral do Sudoku é NP-completo
- **Versão NP?**: Sim, verificar uma solução é O(N²) (polinomial)
- **NP-Completo**: Sudoku generalizado (NxN) é NP-completo

---

## 🔬 Análise Prática vs Teórica

Os resultados práticos demonstram:

1. **Crescimento exponencial** com aumento de células vazias
2. **Diferença significativa** entre melhor e pior caso
3. **Impacto da linguagem** (C geralmente 10-50x mais rápido que Python)
4. **Variabilidade** mesmo com mesma configuração (aleatoriedade do puzzle)

---

## 🎓 Objetivos Educacionais

Este projeto visa:

✅ Compreender **análise de complexidade** na prática  
✅ Comparar **implementações iterativas vs recursivas**  
✅ Analisar **diferenças entre linguagens** (C vs Python)  
✅ Investigar **melhor, pior e caso médio**  
✅ Relacionar **teoria com prática** em algoritmos NP-completos

---

## 👥 Equipe

- [Nome 1]
- [Nome 2]
- [Nome 3]
- [Nome 4]

**Algoritmo sorteado**: Backtracking (Sudoku)  
**Data**: Outubro/Novembro 2025

---

## 📚 Referências

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*
2. Cormen, T. H., et al. (2009). *Introduction to Algorithms*
3. Sudoku Solving Algorithms: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
4. NP-Completeness of Sudoku: Yato, T., & Seta, T. (2003)

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais como parte do curso de Teoria da Computação na CESAR School.

---

## 📧 Contato

Para dúvidas sobre o projeto:
- **Professor**: Daniel Bezerra
- **Disciplina**: Teoria da Computação
- **Instituição**: CESAR School

---

**Última atualização**: Novembro 2025
