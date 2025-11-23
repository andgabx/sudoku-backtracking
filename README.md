# 🧩 Análise de Complexidade: Backtracking Iterativo para Sudoku

## 📋 Descrição do Projeto

Este projeto implementa e analisa a complexidade de tempo do algoritmo de **Backtracking Iterativo** para resolver puzzles de Sudoku. O objetivo é realizar uma análise comparativa detalhada considerando:

- **Duas linguagens de programação**: C e Python
- **Três tamanhos de problema**: Small (3×3), Medium (6×6), Large (9×9)
- **Dois casos de teste**: Melhor caso e Pior caso
- **30 execuções** para cada combinação de parâmetros
- **Medição de tempo** e **contagem de iterações**

### 🎯 Características Principais

✅ **Backtracking Iterativo** (não recursivo) usando lista de células vazias e índice:
   - **C**: Array de coordenadas (`Coordenada[]`) para armazenar células vazias
   - **Python**: Lista de tuplas `Coordenada` para armazenar células vazias

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
│   │   └── backtracking.h     # Algoritmo de backtracking iterativo
│   │
│   └── src/                    # Código fonte (.c)
│       ├── sudoku.c           # Implementação das operações
│       ├── backtracking.c     # Implementação do backtracking
│       ├── puzzle_loader.c    # Carregamento de puzzles de arquivos
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
├── puzzle_seeds/              # Puzzles pré-gerados (criado por generate_sudoku_puzzles.py)
│   ├── small_best.txt        # 30 puzzles para Small Best Case
│   ├── small_worst.txt       # 30 puzzles para Small Worst Case
│   └── ... (6 arquivos no total)
│
├── plot/                       # Scripts de visualização
│   ├── plot_results.py        # Geração de gráficos de performance
│   └── requirements.txt       # Dependências Python
│
├── analyze_results.py          # Script de análise e visualização de resultados
├── generate_sudoku_puzzles.py  # Script para gerar puzzles pré-gerados
├── run_with_shared_seeds.py   # Script para executar testes com puzzles compartilhados
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
- Executa 3 sizes × 2 cases = 6 combinações (C e Python juntos)
- Cada combinação executa 30 testes em C e 30 em Python (com puzzles pré-gerados compartilhados)
- Gera 12 arquivos de log com resultados completos

**ℹ️ Nota**: Os puzzles são gerados automaticamente antes de cada execução. Se quiser gerar manualmente:
```bash
python3 generate_sudoku_puzzles.py
```

**⏱️ Tempo estimado**: 5-15 minutos (dependendo do hardware)

### Fluxo Completo de Execução

Quando você executa `make run-all`, o seguinte fluxo ocorre:

#### 1. Preparação
```
make run-all
    ↓
Verifica/instala dependências Python (pandas, matplotlib, numpy)
    ↓
Compila código C (gcc → c/bin/sudoku_solver)
    ↓
Cria diretório logs/ se não existir
```

#### 2. Para cada combinação (size × case) - Exemplo: Small Best Case

**Passo 2.1: Geração e Carregamento de Puzzles Pré-gerados**
```
run_with_shared_seeds.py small best
    ↓
Gera puzzles (se não existirem) → puzzle_seeds/small_best.txt
    ↓
Carrega arquivo: puzzle_seeds/small_best.txt
    ↓
Arquivo contém 30 puzzles no formato:
  === Puzzle 1/30 ===
  3 | 2 | 0
  ------
  0 | 1 | 3
  ------
  1 | 3 | 2

  === Puzzle 2/30 ===
  ...
```

**Passo 2.2: Execução em C**
```
Executa: c/bin/sudoku_solver small best puzzle_seeds/small_best.txt
    ↓
Lê arquivo de puzzles → Carrega 30 puzzles
    ↓
Loop: Para cada execução (1 a 30):
    ├─ Execução 1:
    │   ├─ Lê Puzzle 1 do arquivo
    │   ├─ Parse do formato texto → Sudoku objeto
    │   ├─ solve_sudoku_iterative() → resolve o puzzle
    │   │   ├─ Encontra células vazias → lista_vazias[]
    │   │   ├─ Loop com índice k:
    │   │   │   ├─ Tenta números válidos
    │   │   │   ├─ Se válido: k++ (avança)
    │   │   │   └─ Se inválido: k-- (backtrack)
    │   │   └─ Retorna: tempo, iterações, resolvido
    │   └─ Salva no log: logs/c_small_best.log
    │
    ├─ Execução 2:
    │   ├─ Lê Puzzle 2 do arquivo
    │   └─ ... (mesmo processo)
    │
    └─ ... (até execução 30)
    ↓
Gera estatísticas finais → Salva em logs/c_small_best.log
```

**Passo 2.3: Execução em Python**
```
Executa: python3 main.py small best puzzle_seeds/small_best.txt
    ↓
Lê arquivo de puzzles → Carrega 30 puzzles
    ↓
Loop: Para cada execução (1 a 30):
    ├─ Execução 1:
    │   ├─ Lê Puzzle 1 do arquivo
    │   ├─ Parse do formato texto → Sudoku objeto (MESMO puzzle que C!)
    │   ├─ solve_sudoku_iterativo() → resolve o puzzle
    │   │   ├─ Encontra células vazias → lista_vazias[]
    │   │   ├─ Loop com índice k:
    │   │   │   ├─ Tenta números válidos
    │   │   │   ├─ Se válido: k += 1 (avança)
    │   │   │   └─ Se inválido: k -= 1 (backtrack)
    │   │   └─ Retorna: tempo, iterações, resolvido
    │   └─ Salva no log: logs/python_small_best.log
    │
    └─ ... (mesmos puzzles que C)
    ↓
Gera estatísticas finais → Salva em logs/python_small_best.log
```

**Resultado:**
- C e Python resolveram os **mesmos 30 puzzles**
- Comparação justa: mesmas iterações, tempos diferentes (performance da linguagem)

#### 3. Repetição para todas as combinações
```
[1/6] Small - Best Case    → puzzle_seeds/small_best.txt
[2/6] Small - Worst Case   → puzzle_seeds/small_worst.txt
[3/6] Medium - Best Case   → puzzle_seeds/medium_best.txt
[4/6] Medium - Worst Case  → puzzle_seeds/medium_worst.txt
[5/6] Large - Best Case    → puzzle_seeds/large_best.txt
[6/6] Large - Worst Case   → puzzle_seeds/large_worst.txt
```

#### 4. Resultados Gerados
```
logs/
├── c_small_best.log      (30 execuções + estatísticas)
├── c_small_worst.log
├── c_medium_best.log
├── c_medium_worst.log
├── c_large_best.log
├── c_large_worst.log
├── python_small_best.log  (30 execuções + estatísticas)
├── python_small_worst.log
├── python_medium_best.log
├── python_medium_worst.log
├── python_large_best.log
└── python_large_worst.log

puzzle_seeds/
├── small_best.txt         (30 puzzles pré-gerados)
├── small_worst.txt
├── medium_best.txt
├── medium_worst.txt
├── large_best.txt
└── large_worst.txt
```

#### 5. Análise e Visualização (Opcional)
```bash
# Analisar resultados
python3 analyze_results.py
    ↓
Lê todos os 12 arquivos de log
    ↓
Extrai estatísticas (tempo médio, iterações médias, etc.)
    ↓
Gera tabelas comparativas

# Gerar gráficos
python3 plot/plot_results.py
    ↓
Lê todos os 12 arquivos de log
    ↓
Gera 4 gráficos PNG em plot/
```

#### Diagrama do Fluxo Completo
```
make run-all
    ↓
┌─────────────────────────────────────────┐
│ Para cada combinação (size × case):   │
│                                         │
│  1. Gerar puzzles → puzzle_seeds/*.txt │
│  2. Executar C:                        │
│     └─ Para cada execução (1-30):      │
│        ├─ Ler puzzle[i] do arquivo     │
│        ├─ Parse puzzle (formato texto) │
│        ├─ Resolver puzzle              │
│        └─ Salvar resultado no log      │
│  3. Executar Python:                   │
│     └─ Para cada execução (1-30):      │
│        ├─ Ler puzzle[i] (MESMO de C!) │
│        ├─ Parse puzzle (MESMO de C!)  │
│        ├─ Resolver puzzle              │
│        └─ Salvar resultado no log      │
└─────────────────────────────────────────┘
    ↓
12 arquivos de log gerados
    ↓
(Opicional) analyze_results.py → Tabelas
(Opicional) plot/plot_results.py → Gráficos
```

### Teste Rápido

```bash
# Teste rápido para validar o funcionamento
make test
```

### Limpeza

```bash
# Remove arquivos compilados, logs e gráficos
make clean

# Remove também os puzzles pré-gerados (incluído em clean)
make clean-all
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

### Geração de Gráficos

```bash
# Gera gráficos de performance a partir dos logs
python3 plot/plot_results.py
```

**Pré-requisitos:**
As dependências Python (pandas, matplotlib, numpy) são instaladas automaticamente quando você executa qualquer comando `make`. Se preferir instalar manualmente:

```bash
pip install pandas matplotlib numpy
```

**Gráficos gerados:**

O script gera 4 gráficos em formato PNG (alta resolução, 300 DPI):

1. **1_tempo_comparacao.png**
   - Comparação de tempo entre C e Python
   - Separado por Best Case e Worst Case
   - Escala logarítmica para melhor visualização
   - Valores formatados de forma legível (μs, ms, s)

2. **2_tempo_vs_iteracoes.png**
   - Gráfico de dispersão (scatter plot) mostrando Tempo vs Iterações
   - Mostra a eficiência de cada linguagem: para a mesma quantidade de iterações, qual executa mais rápido
   - Separado por Best Case e Worst Case
   - **Nota**: Como os puzzles são idênticos, as iterações são sempre iguais entre C e Python. Este gráfico mostra a diferença de performance (tempo) para a mesma quantidade de trabalho (iterações).

3. **3_best_vs_worst.png**
   - Comparação direta entre Best Case e Worst Case
   - Mostra tempo e iterações lado a lado
   - Compara C e Python

4. **4_resumo_desempenho.png**
   - Análise de desempenho comparativa (gráfico de linha)
   - Mostra a evolução do tempo conforme o tamanho aumenta
   - Compara C e Python em Best e Worst Case
   - Similar ao estilo de análise de algoritmos clássicos

**Detalhes técnicos:**
- **Formato de saída**: PNG (300 DPI)
- **Bibliotecas usadas**: pandas, matplotlib, numpy
- **Fonte de dados**: Arquivos de log em `logs/`
- **Localização**: Gráficos salvos em `plot/`

### Puzzles Pré-gerados

O projeto usa um sistema de **puzzles pré-gerados** para garantir que C e Python resolvam os mesmos puzzles, permitindo comparação justa de iterações e performance.

**Como funciona:**
- Os puzzles são gerados uma vez usando Python e salvos em arquivos de texto
- Cada arquivo contém 30 puzzles no formato visual (como são impressos)
- C e Python leem os mesmos arquivos e resolvem os mesmos puzzles

**Geração dos puzzles:**
```bash
# Gera todos os arquivos de puzzles (executado automaticamente antes de cada teste)
python3 generate_sudoku_puzzles.py
```

Este comando gera 6 arquivos em `puzzle_seeds/`:
- `small_best.txt` - 30 puzzles 3×3 com 2 células vazias
- `small_worst.txt` - 30 puzzles 3×3 com 5 células vazias
- `medium_best.txt` - 30 puzzles 6×6 com 9 células vazias
- `medium_worst.txt` - 30 puzzles 6×6 com 22 células vazias
- `large_best.txt` - 30 puzzles 9×9 com 23 células vazias
- `large_worst.txt` - 30 puzzles 9×9 com 55 células vazias

**Formato dos arquivos:**
Cada arquivo `.txt` contém 30 puzzles no formato visual:
```
=== Puzzle 1/30 ===
3 | 2 | 0
------
0 | 1 | 3
------
1 | 3 | 2

=== Puzzle 2/30 ===
0 | 3 | 1
------
1 | 2 | 3
------
3 | 1 | 0

...
```

**Vantagens:**
- **Garantia total**: C e Python resolvem exatamente os mesmos puzzles
- **Reprodutibilidade**: Os puzzles são salvos permanentemente
- **Simplicidade**: Não depende de geradores aleatórios compatíveis entre linguagens
- **Transparência**: Você pode ver exatamente quais puzzles estão sendo resolvidos

**Uso:**
Os puzzles são gerados uma vez e reutilizados em todas as execuções. Para regenerar os puzzles (com novos valores aleatórios), execute novamente:
```bash
python3 generate_sudoku_puzzles.py
```

**Limpeza:**
Para remover os puzzles pré-gerados, use:
```bash
make clean-all
```

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

Ao contrário da implementação recursiva tradicional, este projeto usa **backtracking iterativo** baseado em lista de células vazias e índice de navegação:

#### C - Lista de Coordenadas
```c
typedef struct {
    int row;
    int col;
} Coordenada;

Coordenada* lista_vazias = malloc(sizeof(Coordenada) * size * size);
int k = 0;  // Índice da célula vazia atual
```

#### Python - Lista de Coordenadas
```python
class Coordenada(NamedTuple):
    row: int
    col: int

lista_vazias = []  # Lista de Coordenada
k = 0  # Índice da célula vazia atual
```

### Fluxo do Algoritmo

1. **Inicialização**: 
   - Encontra todas as células vazias e armazena em uma lista de coordenadas
   - Inicializa índice `k = 0` (primeira célula vazia)

2. **Loop Principal**: Enquanto `0 ≤ k < total_vazias`:
   - Obtém a célula vazia atual: `lista_vazias[k]`
   - Tenta números a partir do valor atual da célula + 1 até N
   - Se encontrar número válido:
     - Coloca o número na célula
     - Incrementa `k++` (avança para próxima célula vazia)
     - Se `k == total_vazias` → **Resolvido!**
   - Se não encontrar número válido:
     - Limpa a célula (`grid[r][c] = 0`)
     - Decrementa `k--` (backtrack para célula anterior)

3. **Fim**: 
   - Se `k == total_vazias`: Sudoku resolvido
   - Se `k < 0`: Impossível resolver (backtrack completo)

### Vantagens da Implementação Iterativa

✅ **Controle explícito** do estado do algoritmo através do índice `k`  
✅ **Sem limite de recursão** (evita stack overflow)  
✅ **Contagem precisa** de iterações  
✅ **Estrutura simples**: apenas uma lista de coordenadas e um índice  
✅ **Mais eficiente** em algumas linguagens (menos overhead que recursão)

---

## 📈 Análise de Complexidade

### Classificação Assintótica

- **Pior Caso**: O(N^M) onde:
  - N = tamanho do Sudoku (3, 6, 9)
  - M = número de células vazias

- **Melhor Caso**: O(M) onde M é o número de células vazias (quando não há backtracking necessário)

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
✅ Investigar **melhor, pior caso**  
✅ Relacionar **teoria com prática** em algoritmos NP-completos

---

## 👥 Equipe

- Anderson Gabriel
- Débora Souza
- Filipe Macedo
- Rafael Peixoto


---

## 📚 Referências

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*
2. Cormen, T. H., et al. (2009). *Introduction to Algorithms*
3. Sudoku Solving Algorithms: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
4. NP-Completeness of Sudoku: Yato, T., & Seta, T. (2003)
5. Randomness in Sudoku solving algorithm: https://stackoverflow.com/questions/60813855/randomness-in-sudoku-solving-algorithm