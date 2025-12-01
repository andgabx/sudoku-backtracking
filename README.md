# 🧩 Análise de Complexidade: Backtracking Iterativo para Sudoku

## 📋 Descrição do Projeto

Este projeto implementa e analisa a complexidade de tempo do algoritmo de **Backtracking Iterativo** para resolver puzzles de Sudoku. O objetivo é realizar uma análise comparativa detalhada considerando:

- **Duas linguagens de programação**: C e Python
- **Três tamanhos de problema**: Small (4×4), Medium (9×9), Large (16×16)
- **Dois casos de teste**: Melhor caso e Pior caso
- **30 execuções** para cada combinação de parâmetros
- **Medição de tempo** e **contagem de iterações**

### 🎯 Características Principais

✅ **Backtracking Iterativo** (não recursivo) usando lista de células vazias e índice:
   - **C**: Array de coordenadas (`Coordenada[]`) para armazenar células vazias
   - **Python**: Lista de tuplas `Coordenada` para armazenar células vazias

✅ **Heurística MRV (Minimum Remaining Values)**: Otimiza a escolha da próxima célula vazia, priorizando células com menos valores possíveis, reduzindo significativamente o espaço de busca

✅ **Gerador de Puzzles em C** com configurações controladas de dificuldade, usando LCG (Linear Congruential Generator) para garantir puzzles válidos

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
│   │   ├── backtracking.h     # Algoritmo de backtracking iterativo e heurística MRV
│   │   └── generator.h        # Gerador de puzzles (LCG, fill_sudoku, generate_sudoku)
│   │
│   └── src/                    # Código fonte (.c)
│       ├── main.c             # ← Função principal do código em C
│       │                        #    - Processa argumentos de linha de comando
│       │                        #    - Carrega puzzles de arquivos
│       │                        #    - Executa 30 testes por configuração
│       │                        #    - Chama solve_sudoku_iterative() para cada puzzle
│       │                        #    - Gera logs com resultados (tempo, iterações)
│       │
│       ├── backtracking.c     # ← Implementação do algoritmo de backtracking iterativo
│       │                        #    - solve_sudoku_iterative(): algoritmo principal com MRV
│       │                        #    - find_all_empty_cells(): encontra células vazias
│       │                        #    - find_next_valid_number(): busca próximo valor válido
│       │                        #    - count_possible_values(): conta valores possíveis (MRV)
│       │                        #    - sort_empty_cells_by_mrv(): ordena células por MRV
│       │                        #    - is_safe(), is_in_row(), is_in_col(), is_in_box(): validações
│       │
│       ├── sudoku.c           # ← Implementação das operações básicas do Sudoku
│       │                        #    - sudoku_create(): cria estrutura do Sudoku
│       │                        #    - sudoku_destroy(): libera memória
│       │                        #    - is_valid(): verifica se número é válido
│       │                        #    - sudoku_print(): imprime o Sudoku
│       │                        #    - count_empty_cells(): conta células vazias
│       │                        #    - sudoku_parse_from_string(): converte string para Sudoku
│       │                        #    - num_to_char(), char_to_num(): conversão 1-9 e A-G
│       │
│       ├── puzzle_loader.c    # ← Carregamento de puzzles de arquivos
│       │                        #    - load_puzzle_from_file(): lê um puzzle do arquivo
│       │                        #    - Parse do formato texto (com separadores | e -)
│       │                        #    - Retorna Sudoku pronto para resolução
│       │
│       ├── generator.c        # ← Implementação do gerador de puzzles
│       │                        #    - lcg_seed(), lcg_next(): Linear Congruential Generator
│       │                        #    - shuffle(): algoritmo Fisher-Yates
│       │                        #    - fill_sudoku(): preenche Sudoku completo recursivamente
│       │                        #    - generate_sudoku(): gera puzzle com células vazias
│       │                        #    - sudoku_to_string(): converte Sudoku para formato texto
│       │
│       └── puzzle_generator.c # ← Programa principal para gerar arquivos de puzzles
│                                #    - generate_puzzles_for_config(): gera 30 puzzles por config
│                                #    - Salva puzzles em puzzle_seeds/{size}_{case}.txt
│
├── python/                     # Implementação em Python
│   └── src/                    # Módulos Python
│       ├── main.py            # ← Função principal do código em Python
│       │                        #    - Processa argumentos de linha de comando
│       │                        #    - Carrega puzzles de arquivos
│       │                        #    - Executa 30 testes por configuração
│       │                        #    - Chama solve_sudoku_iterativo() para cada puzzle
│       │                        #    - Gera logs com resultados (tempo, iterações)
│       │
│       ├── backtracking.py    # ← Algoritmo de backtracking iterativo
│       │                        #    - solve_sudoku_iterativo(): algoritmo principal com MRV
│       │                        #    - _find_all_empty_cells(): encontra células vazias
│       │                        #    - _find_next_valid_number(): busca próximo valor válido
│       │                        #    - _count_possible_values(): conta valores possíveis (MRV)
│       │                        #    - _sort_empty_cells_by_mrv(): ordena células por MRV
│       │                        #    - _is_safe(), _is_in_row(), _is_in_col(), _is_in_box(): validações
│       │
│       ├── sudoku.py          # ← Classe Sudoku e operações básicas
│       │                        #    - Classe Sudoku: estrutura de dados
│       │                        #    - is_valid(): verifica se número é válido
│       │                        #    - print(): imprime o Sudoku
│       │                        #    - count_empty_cells(): conta células vazias
│       │                        #    - parse_from_string(): converte string para Sudoku
│       │
│
│
├── logs/                       # Logs gerados (criado automaticamente)
│   ├── c_small_best.log
│   ├── c_small_worst.log
│   ├── python_small_best.log
│   └── ... (12 arquivos no total)
│
├── puzzle_seeds/              # Puzzles pré-gerados (criado por puzzle_generator em C)
│   ├── small_best.txt        # 30 puzzles para Small Best Case
│   ├── small_worst.txt       # 30 puzzles para Small Worst Case
│   └── ... (6 arquivos no total)
│
├── plot/                       # Scripts de visualização
│   ├── plot_results.py        # ← Geração de gráficos de performance
│   │                            #    - Lê arquivos de log
│   │                            #    - Gera 4 gráficos PNG (tempo, iterações, comparações)
│   │                            #    - Usa pandas, matplotlib, numpy
│   │
│   └── requirements.txt       # Dependências Python
│
├── analyze_results.py          # ← Script de análise e visualização de resultados
│                                #    - Lê todos os arquivos de log
│                                #    - Extrai estatísticas (tempo médio, iterações)
│                                #    - Gera tabelas comparativas C vs Python
│                                #    - Calcula speedup entre linguagens
│
│
│
├── run_with_shared_seeds.py   # ← Script para executar testes com puzzles compartilhados
│                                #    - Orquestra execução de C e Python
│                                #    - Garante que ambos usem os mesmos puzzles
│                                #    - Usado pelo Makefile em run-all e test
│
├── Makefile                    # ← Automação de compilação e testes
│                                #    - build: compila código C
│                                #    - run: executa teste específico
│                                #    - run-all: executa todos os 360 testes
│                                #    - test: teste rápido
│                                #    - clean: remove arquivos gerados
│
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

**ℹ️ Nota**: Os puzzles são gerados automaticamente antes de cada execução usando o gerador em C. Se quiser gerar manualmente:
```bash
make build-generator
./c/bin/puzzle_generator
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
- Os puzzles são gerados uma vez usando C e salvos em arquivos de texto
- Cada arquivo contém 30 puzzles no formato visual (como são impressos)
- C e Python leem os mesmos arquivos e resolvem os mesmos puzzles

**Geração dos puzzles:**
```bash
# Gera todos os arquivos de puzzles (executado automaticamente antes de cada teste)
make build-generator
./c/bin/puzzle_generator
```

Este comando gera 6 arquivos em `puzzle_seeds/`:
- `small_best.txt` - 30 puzzles 4×4 com 5 células vazias (31%) - mais fácil
- `small_worst.txt` - 30 puzzles 4×4 com 8 células vazias (50%) - mais difícil
- `medium_best.txt` - 30 puzzles 9×9 com 24 células vazias (30%) - mais fácil
- `medium_worst.txt` - 30 puzzles 9×9 com 40 células vazias (49%) - mais difícil
- `large_best.txt` - 30 puzzles 16×16 com 77 células vazias (30%) - mais fácil
- `large_worst.txt` - 30 puzzles 16×16 com 128 células vazias (50%) - mais difícil

**Formato dos arquivos:**
Cada arquivo `.txt` contém 30 puzzles no formato visual. Para Sudokus 16×16, números de 10-16 são representados como A-G:
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

=== Puzzle 1/30 (16×16) ===
1 | 2 | 3 | A
4 | 5 | 6 | B
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
make build-generator
./c/bin/puzzle_generator
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
| Small   | 4×4      | 5 (31%)              | 8 (50%)             |
| Medium  | 9×9      | 24 (30%)             | 40 (49%)            |
| Large   | 16×16    | 77 (30%)             | 128 (50%)           |

**Melhor Caso**: Puzzles com aproximadamente 30% das células vazias. O algoritmo encontra a solução mais rapidamente, com menos backtracking, pois há menos células para preencher. A heurística MRV ajuda a processar células mais restritas primeiro, encontrando conflitos mais cedo.

**Pior Caso**: Puzzles com aproximadamente 50% das células vazias. Estes são mais difíceis de resolver, exigindo mais backtracking e iterações, pois há mais células para preencher e mais combinações possíveis. A heurística MRV é especialmente benéfica nestes casos, reduzindo significativamente o espaço de busca.

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

Coordenada* lista_vazias = (Coordenada*)malloc(
    sizeof(Coordenada) * sudoku->size * sudoku->size);
int total_vazias = find_all_empty_cells(sudoku, lista_vazias);
int k = 0;  // Índice da célula vazia atual
```

#### Python - Lista de Coordenadas
```python
class Coordenada(NamedTuple):
    row: int
    col: int

lista_vazias = _find_all_empty_cells(sudoku)  # Lista de Coordenada
total_vazias = len(lista_vazias)
k = 0  # Índice da célula vazia atual
```

### Fluxo do Algoritmo

1. **Inicialização**: 
   - Encontra todas as células vazias usando `find_all_empty_cells()` (C) ou `_find_all_empty_cells()` (Python)
   - Armazena as coordenadas em `lista_vazias` e obtém `total_vazias`
   - **Ordena células vazias por MRV** (Minimum Remaining Values): células com menos valores possíveis são processadas primeiro
   - Inicializa índice `k = 0` (primeira célula vazia)
   - Se `total_vazias == 0`, o Sudoku já está resolvido

2. **Loop Principal**: Enquanto `k >= 0 && k < total_vazias` (C) ou `-1 < k < total_vazias` (Python):
   - Obtém a célula vazia atual: `lista_vazias[k]`
   - Extrai coordenadas: `r = cell.row`, `c = cell.col`
   - Calcula início da busca: `num_inicio = grid[r][c] + 1`
   - Busca próximo número válido: `num_valido = find_next_valid_number(sudoku, r, c, num_inicio)`
   - Se encontrar número válido (`num_valido <= size`):
     - Coloca o número na célula: `grid[r][c] = num_valido`
     - Incrementa `k++` (avança para próxima célula vazia)
     - **Reordena células restantes por MRV** (apenas quando avançamos, não durante backtracking)
     - Se `k == total_vazias` → **Resolvido!**
   - Se não encontrar número válido (`num_valido > size`):
     - Limpa a célula: `grid[r][c] = 0` (backtrack)
     - Decrementa `k--` (recua para célula anterior)

3. **Fim**: 
   - Se `k == total_vazias`: Sudoku resolvido
   - Se `k < 0`: Impossível resolver (backtrack completo)

### Vantagens da Implementação Iterativa

✅ **Controle explícito** do estado do algoritmo através do índice `k`  
✅ **Sem limite de recursão** (evita stack overflow)  
✅ **Contagem precisa** de iterações  
✅ **Estrutura simples**: apenas uma lista de coordenadas e um índice  
✅ **Mais eficiente** em algumas linguagens (menos overhead que recursão)  
✅ **Heurística MRV**: Reduz drasticamente o espaço de busca ao priorizar células mais restritas

---

## 📈 Análise de Complexidade

### Classificação Assintótica

- **Pior Caso**: O(N^M) onde:
  - N = tamanho do Sudoku (4, 9, 16) - número de possíveis valores por célula
  - M = número de células vazias
  - **Quando ocorre**: Quando o algoritmo precisa explorar muitas combinações de valores para as células vazias. Isso acontece quando os valores corretos só são encontrados após testar muitas combinações inválidas, exigindo backtracking extensivo.
  - **Com heurística MRV**: A complexidade prática é significativamente reduzida, pois células mais restritas são processadas primeiro, encontrando conflitos mais cedo e reduzindo o espaço de busca explorado.

- **Melhor Caso**: O(M) onde M é o número de células vazias
  - **Quando ocorre**: Quando o algoritmo encontra a solução sem necessidade de backtracking significativo. Isso acontece quando os valores corretos são encontrados rapidamente para cada célula, resultando em complexidade linear no número de células vazias.
  - **Com heurística MRV**: A performance é ainda melhor, pois a ordenação inicial já coloca as células mais fáceis de resolver primeiro.

### Classes de Complexidade

- **Classe P?**: Não, o problema geral do Sudoku é NP-completo
- **Versão NP?**: Sim, verificar uma solução é O(N²) (polinomial)
- **NP-Completo**: Sudoku generalizado (NxN) é NP-completo

---

## 🔬 Análise Prática vs Teórica

Os resultados práticos demonstram:

1. **Crescimento exponencial** com aumento de células vazias, confirmando a complexidade O(N^M) no pior caso
2. **Diferença significativa** entre melhor e pior caso: a razão worst/best aumenta drasticamente com o tamanho do Sudoku, demonstrando que o crescimento exponencial se torna dominante em problemas maiores
3. **Impacto da linguagem**: C apresenta speedup significativo em relação a Python, variando conforme a complexidade do problema
4. **Variabilidade** mesmo com mesma configuração: puzzles diferentes com mesmo número de células vazias podem ter complexidades muito diferentes, dependendo da distribuição e da ordem das células vazias
5. **Heurística MRV**: A implementação da heurística MRV reduz significativamente o número de iterações e o tempo de execução, especialmente para puzzles mais difíceis, ao priorizar células com menos opções

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