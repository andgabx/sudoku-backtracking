
# Variáveis
CC = gcc
CFLAGS = -Wall -Wextra -O2 -lm
PYTHON = python3

# Diretórios
C_SRC_DIR = c/src
C_INC_DIR = c/include
C_BIN_DIR = c/bin
PY_SRC_DIR = python/src
LOGS_DIR = logs

# Arquivos fonte C
C_SOURCES = $(C_SRC_DIR)/sudoku.c $(C_SRC_DIR)/backtracking.c $(C_SRC_DIR)/generator.c $(C_SRC_DIR)/main.c
C_EXECUTABLE = $(C_BIN_DIR)/sudoku_solver

# Parâmetros padrão
SIZE ?= small
CASE ?= best
LANG ?= c

# Cores para output
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[1;33m
NC = \033[0m # No Color

.PHONY: all build clean run run-all help test

# Target padrão
all: help

# Compila o código C
build:
	@echo "$(BLUE)Compilando código C...$(NC)"
	@mkdir -p $(C_BIN_DIR)
	@$(CC) $(C_SOURCES) -I$(C_INC_DIR) -o $(C_EXECUTABLE) $(CFLAGS)
	@echo "$(GREEN)✓ Compilação concluída!$(NC)"

# Cria diretório de logs
$(LOGS_DIR):
	@mkdir -p $(LOGS_DIR)

# Executa um teste específico
run: $(LOGS_DIR)
ifeq ($(LANG),c)
	@$(MAKE) build --no-print-directory
	@echo "$(BLUE)Executando teste C: SIZE=$(SIZE) CASE=$(CASE)$(NC)"
	@cd $(C_BIN_DIR) && ./sudoku_solver $(SIZE) $(CASE)
else ifeq ($(LANG),python)
	@echo "$(BLUE)Executando teste Python: SIZE=$(SIZE) CASE=$(CASE)$(NC)"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py $(SIZE) $(CASE)
else
	@echo "$(YELLOW)Erro: LANG deve ser 'c' ou 'python'$(NC)"
	@exit 1
endif

# Executa todas as 12 combinações (3 sizes × 2 cases × 2 langs)
run-all: $(LOGS_DIR)
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Análise Completa de Complexidade - Backtracking Sudoku$(NC)"
	@echo "$(GREEN)  Executando 12 combinações (3 sizes × 2 cases × 2 langs)$(NC)"
	@echo "$(GREEN)  Total: 360 execuções (30 por combinação)$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) build --no-print-directory
	@echo ""
	@echo "$(YELLOW)[1/12]$(NC) Executando: C - Small - Best Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver small best
	@echo ""
	@echo "$(YELLOW)[2/12]$(NC) Executando: C - Small - Worst Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver small worst
	@echo ""
	@echo "$(YELLOW)[3/12]$(NC) Executando: C - Medium - Best Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver medium best
	@echo ""
	@echo "$(YELLOW)[4/12]$(NC) Executando: C - Medium - Worst Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver medium worst
	@echo ""
	@echo "$(YELLOW)[5/12]$(NC) Executando: C - Large - Best Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver large best
	@echo ""
	@echo "$(YELLOW)[6/12]$(NC) Executando: C - Large - Worst Case"
	@cd $(C_BIN_DIR) && ./sudoku_solver large worst
	@echo ""
	@echo "$(YELLOW)[7/12]$(NC) Executando: Python - Small - Best Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py small best
	@echo ""
	@echo "$(YELLOW)[8/12]$(NC) Executando: Python - Small - Worst Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py small worst
	@echo ""
	@echo "$(YELLOW)[9/12]$(NC) Executando: Python - Medium - Best Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py medium best
	@echo ""
	@echo "$(YELLOW)[10/12]$(NC) Executando: Python - Medium - Worst Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py medium worst
	@echo ""
	@echo "$(YELLOW)[11/12]$(NC) Executando: Python - Large - Best Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py large best
	@echo ""
	@echo "$(YELLOW)[12/12]$(NC) Executando: Python - Large - Worst Case"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py large worst
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✓ Análise completa finalizada!$(NC)"
	@echo "$(GREEN)  Logs salvos em: $(LOGS_DIR)/$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@ls -lh $(LOGS_DIR)/

# Testa uma configuração específica (apenas 3 execuções para teste rápido)
test: $(LOGS_DIR)
	@echo "$(BLUE)Teste rápido: C - Small - Best Case (apenas 3 execuções)$(NC)"
	@$(MAKE) build --no-print-directory
	@cd $(C_BIN_DIR) && ./sudoku_solver small best | head -5
	@echo ""
	@echo "$(BLUE)Teste rápido: Python - Small - Best Case (apenas 3 execuções)$(NC)"
	@cd $(PY_SRC_DIR) && $(PYTHON) main.py small best | head -5

# Remove arquivos compilados e logs
clean:
	@echo "$(YELLOW)Removendo arquivos compilados e logs...$(NC)"
	@rm -rf $(C_BIN_DIR) $(LOGS_DIR)
	@echo "$(GREEN)✓ Limpeza concluída!$(NC)"

# Exibe ajuda
help:
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Makefile - Análise de Complexidade de Backtracking$(NC)"
	@echo "$(GREEN)  Projeto de Teoria da Computação - CESAR School$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(BLUE)Comandos disponíveis:$(NC)"
	@echo "  make build           - Compila o código C"
	@echo "  make run             - Executa um teste específico"
	@echo "  make run-all         - Executa TODAS as 12 combinações (360 testes)"
	@echo "  make test            - Teste rápido da configuração"
	@echo "  make clean           - Remove arquivos compilados e logs"
	@echo "  make help            - Exibe esta ajuda"
	@echo ""
	@echo "$(BLUE)Parâmetros para 'make run':$(NC)"
	@echo "  SIZE=small|medium|large    (padrão: small)"
	@echo "  CASE=best|worst            (padrão: best)"
	@echo "  LANG=c|python              (padrão: c)"
	@echo ""
	@echo "$(BLUE)Exemplos de uso:$(NC)"
	@echo "  make run SIZE=small CASE=best LANG=c"
	@echo "  make run SIZE=large CASE=worst LANG=python"
	@echo "  make run-all"
	@echo ""
	@echo "$(BLUE)Configurações dos casos:$(NC)"
	@echo "  Small (3x3):  Best=2-3 vazias  | Worst=5-6 vazias"
	@echo "  Medium (6x6): Best=8-10 vazias | Worst=20-24 vazias"
	@echo "  Large (9x9):  Best=20-25 vazias| Worst=50-60 vazias"
	@echo ""
	@echo "$(YELLOW)Nota: Cada teste executa 30 iterações e gera logs em $(LOGS_DIR)/$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
