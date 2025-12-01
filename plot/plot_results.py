#!/usr/bin/env python3
"""
Script para gerar gráficos de performance do algoritmo de backtracking iterativo para Sudoku.
Compara performance entre C e Python, diferentes tamanhos e casos (best/worst).
"""

import os
import re
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def format_time(value):
    """Formata valores de tempo de forma legível."""
    if value == 0:
        return "0"
    if value < 1e-6:
        return f"{value*1e9:.2f}ns"
    elif value < 1e-3:
        return f"{value*1e6:.2f}μs"
    elif value < 1:
        return f"{value*1e3:.2f}ms"
    else:
        return f"{value:.3f}s"

def format_time_ms_only(value):
    """Formata valores de tempo sempre em milissegundos."""
    if value == 0:
        return "0.00ms"
    # Converter sempre para ms
    ms_value = value * 1000
    # Formatar com precisão adequada
    if ms_value < 0.01:
        return f"{ms_value:.4f}ms".rstrip('0').rstrip('.')
    elif ms_value < 0.1:
        return f"{ms_value:.3f}ms".rstrip('0').rstrip('.')
    elif ms_value < 1:
        return f"{ms_value:.2f}ms"
    else:
        return f"{ms_value:.2f}ms"

# Configuração de estilo
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except OSError:
    try:
        plt.style.use('seaborn-darkgrid')
    except OSError:
        plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

def parse_log_file(filename):
    """Extrai dados estatísticos de um arquivo de log."""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        content = f.read()
    
    lang_match = re.search(r'Linguagem: (\w+)', content)
    size_match = re.search(r'Tamanho: (\d+)x\d+', content)
    case_match = re.search(r'Caso: (\w+)', content)
    success_match = re.search(r'Resoluções bem-sucedidas: (\d+)/(\d+)', content)
    avg_time_match = re.search(r'Tempo médio: ([\d.]+) segundos', content)
    avg_iter_match = re.search(r'Iterações médias: ([\d.]+)', content)
    
    return {
        'language': lang_match.group(1) if lang_match else 'N/A',
        'size': int(size_match.group(1)) if size_match else 0,
        'case': case_match.group(1) if case_match else 'N/A',
        'successful': int(success_match.group(1)) if success_match else 0,
        'total_runs': int(success_match.group(2)) if success_match else 0,
        'avg_time': float(avg_time_match.group(1)) if avg_time_match else 0.0,
        'avg_iterations': float(avg_iter_match.group(1)) if avg_iter_match else 0.0
    }

def load_data(logs_dir):
    """Carrega todos os dados dos logs e retorna um DataFrame."""
    configs = [
        ('c', 'small', 'best'),
        ('c', 'small', 'worst'),
        ('c', 'medium', 'best'),
        ('c', 'medium', 'worst'),
        ('c', 'large', 'best'),
        ('c', 'large', 'worst'),
        ('python', 'small', 'best'),
        ('python', 'small', 'worst'),
        ('python', 'medium', 'best'),
        ('python', 'medium', 'worst'),
        ('python', 'large', 'best'),
        ('python', 'large', 'worst'),
    ]
    
    results = []
    for lang, size, case in configs:
        filename = logs_dir / f"{lang}_{size}_{case}.log"
        data = parse_log_file(filename)
        if data:
            data['lang'] = lang
            data['size_str'] = size
            results.append(data)
    
    if not results:
        return None
    
    df = pd.DataFrame(results)
    return df

def plot_time_comparison(df, output_dir):
    """Gráfico 1: Comparação de tempo entre C e Python por tamanho e caso."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    sizes = sorted(df['size'].unique())
    size_labels = {4: 'Small (4×4)', 9: 'Medium (9×9)', 16: 'Large (16×16)'}
    
    # Gráfico 1: Best Case
    ax1 = axes[0]
    x = np.arange(len(sizes))
    width = 0.35
    
    c_best = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]['avg_time'].values[0] 
              if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]) > 0 else 0 
              for s in sizes]
    py_best = [df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]['avg_time'].values[0] 
               if len(df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]) > 0 else 0 
               for s in sizes]
    
    bars1 = ax1.bar(x - width/2, c_best, width, label='C', color='#2E86AB', alpha=0.8)
    bars2 = ax1.bar(x + width/2, py_best, width, label='Python', color='#A23B72', alpha=0.8)
    
    ax1.set_xlabel('Tamanho do Sudoku', fontweight='bold')
    ax1.set_ylabel('Tempo Médio (ms)', fontweight='bold')
    ax1.set_title('Comparação de Tempo - Best Case', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([size_labels[s] for s in sizes])
    ax1.legend()
    # Converter valores do eixo Y para ms
    ax1.set_yscale('log')
    # Criar formatter para mostrar valores em ms (convertendo de segundos)
    def ms_formatter(x, pos):
        ms_val = x * 1000
        if ms_val < 0.01:
            return f'{ms_val:.4f}'
        elif ms_val < 0.1:
            return f'{ms_val:.3f}'
        elif ms_val < 1:
            return f'{ms_val:.2f}'
        else:
            return f'{ms_val:.1f}'
    ax1.yaxis.set_major_formatter(FuncFormatter(ms_formatter))
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras (sempre em ms)
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        format_time_ms_only(height),
                        ha='center', va='bottom', fontsize=7)
    
    # Gráfico 2: Worst Case
    ax2 = axes[1]
    
    c_worst = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]['avg_time'].values[0] 
               if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]) > 0 else 0 
               for s in sizes]
    py_worst = [df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]['avg_time'].values[0] 
                if len(df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]) > 0 else 0 
                for s in sizes]
    
    bars3 = ax2.bar(x - width/2, c_worst, width, label='C', color='#2E86AB', alpha=0.8)
    bars4 = ax2.bar(x + width/2, py_worst, width, label='Python', color='#A23B72', alpha=0.8)
    
    ax2.set_xlabel('Tamanho do Sudoku', fontweight='bold')
    ax2.set_ylabel('Tempo Médio (ms)', fontweight='bold')
    ax2.set_title('Comparação de Tempo - Worst Case', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([size_labels[s] for s in sizes])
    ax2.legend()
    # Converter valores do eixo Y para ms
    ax2.set_yscale('log')
    # Criar formatter para mostrar valores em ms (convertendo de segundos)
    def ms_formatter(x, pos):
        ms_val = x * 1000
        if ms_val < 0.01:
            return f'{ms_val:.4f}'
        elif ms_val < 0.1:
            return f'{ms_val:.3f}'
        elif ms_val < 1:
            return f'{ms_val:.2f}'
        else:
            return f'{ms_val:.1f}'
    ax2.yaxis.set_major_formatter(FuncFormatter(ms_formatter))
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras (sempre em ms)
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        format_time_ms_only(height),
                        ha='center', va='bottom', fontsize=7)
    
    plt.tight_layout()
    plt.savefig(output_dir / '1_tempo_comparacao.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 1 salvo: 1_tempo_comparacao.png")

def plot_time_vs_iterations(df, output_dir):
    """Gráfico 2: Tempo vs Iterações - Eficiência de cada linguagem."""
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    sizes = sorted(df['size'].unique())
    size_labels = {4: 'Small (4×4)', 9: 'Medium (9×9)', 16: 'Large (16×16)'}
    colors_c = {3: '#2E86AB', 6: '#1B5E7A', 9: '#0D3B5A'}
    colors_py = {3: '#A23B72', 6: '#7A2B54', 9: '#521C36'}
    
    def format_time_label(value):
        """Formata tempo para label"""
        if value < 0.01:
            return f'{value:.4f}ms'
        elif value < 0.1:
            return f'{value:.3f}ms'
        elif value < 1:
            return f'{value:.2f}ms'
        else:
            return f'{value:.2f}ms'
    
    def format_iter_label(value):
        """Formata iterações para label"""
        if value < 1:
            return f'{value:.2f}'
        elif value < 1000:
            return f'{int(value)}'
        else:
            return f'{int(value/1000)}k'
    
    # Best Case
    ax1 = axes[0]
    
    for s in sizes:
        c_data = df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]
        py_data = df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]
        
        if len(c_data) > 0 and len(py_data) > 0:
            c_iter = c_data['avg_iterations'].values[0]
            c_time = c_data['avg_time'].values[0] * 1000  # ms
            py_iter = py_data['avg_iterations'].values[0]
            py_time = py_data['avg_time'].values[0] * 1000  # ms
            
            # Plotar pontos
            ax1.scatter(c_iter, c_time, s=300, marker='s', 
                       color=colors_c[s], alpha=0.8, edgecolors='black', linewidth=2, zorder=3)
            ax1.scatter(py_iter, py_time, s=300, marker='o', 
                       color=colors_py[s], alpha=0.8, edgecolors='black', linewidth=2, zorder=3)
            
            # Linha conectando C e Python para o mesmo tamanho
            ax1.plot([c_iter, py_iter], [c_time, py_time], 'k--', alpha=0.4, linewidth=1.5, zorder=1)
            
            # Labels com valores explícitos - posicionamento inteligente
            # Label para C (à esquerda do ponto se for Small, acima se for Medium/Large)
            offset_x_c = -35 if s == 3 else 0
            offset_y_c = 25 if s == 3 else 30
            ax1.annotate(f'C {size_labels[s]}\nTempo: {format_time_label(c_time)}\nIter: {format_iter_label(c_iter)}',
                        xy=(c_iter, c_time), xytext=(offset_x_c, offset_y_c),
                        textcoords='offset points', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor=colors_c[s], alpha=0.95, edgecolor='black', linewidth=2),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2, color='black'))
            
            # Label para Python (à direita do ponto se for Small, acima se for Medium/Large)
            offset_x_py = 35 if s == 3 else 0
            offset_y_py = 25 if s == 3 else 30
            ax1.annotate(f'Python {size_labels[s]}\nTempo: {format_time_label(py_time)}\nIter: {format_iter_label(py_iter)}',
                        xy=(py_iter, py_time), xytext=(offset_x_py, offset_y_py),
                        textcoords='offset points', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor=colors_py[s], alpha=0.95, edgecolor='black', linewidth=2),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2, color='black'))
    
    ax1.set_xlabel('Iterações Médias', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Tempo Médio (ms) - Escala Log', fontweight='bold', fontsize=12)
    ax1.set_title('Tempo vs Iterações - Best Case\nEficiência: Menor tempo para mesma iteração = Mais eficiente', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_yscale('log')
    
    # Adicionar legenda explicativa
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2E86AB', edgecolor='black', label='C (Compilado)'),
        Patch(facecolor='#A23B72', edgecolor='black', label='Python (Interpretado)'),
        plt.Line2D([0], [0], color='black', linestyle='--', linewidth=1.5, label='Mesmo puzzle (iterações iguais)')
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)
    
    # Worst Case
    ax2 = axes[1]
    
    for s in sizes:
        c_data = df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]
        py_data = df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]
        
        if len(c_data) > 0 and len(py_data) > 0:
            c_iter = c_data['avg_iterations'].values[0]
            c_time = c_data['avg_time'].values[0] * 1000  # ms
            py_iter = py_data['avg_iterations'].values[0]
            py_time = py_data['avg_time'].values[0] * 1000  # ms
            
            # Plotar pontos
            ax2.scatter(c_iter, c_time, s=300, marker='s', 
                       color=colors_c[s], alpha=0.8, edgecolors='black', linewidth=2, zorder=3)
            ax2.scatter(py_iter, py_time, s=300, marker='o', 
                       color=colors_py[s], alpha=0.8, edgecolors='black', linewidth=2, zorder=3)
            
            # Linha conectando C e Python para o mesmo tamanho
            ax2.plot([c_iter, py_iter], [c_time, py_time], 'k--', alpha=0.4, linewidth=1.5, zorder=1)
            
            # Labels com valores explícitos - posicionamento inteligente para evitar sobreposição
            # No Worst Case, Small e Medium têm iterações muito próximas, então precisamos de offsets maiores
            if s == 3:  # Small
                offset_x_c = -50
                offset_y_c = 20
                offset_x_py = 50
                offset_y_py = 20
            elif s == 6:  # Medium
                offset_x_c = -45
                offset_y_c = 35
                offset_x_py = 45
                offset_y_py = 35
            else:  # Large
                offset_x_c = 0
                offset_y_c = 40
                offset_x_py = 0
                offset_y_py = 40
            
            ax2.annotate(f'C {size_labels[s]}\nTempo: {format_time_label(c_time)}\nIter: {format_iter_label(c_iter)}',
                        xy=(c_iter, c_time), xytext=(offset_x_c, offset_y_c),
                        textcoords='offset points', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor=colors_c[s], alpha=0.95, edgecolor='black', linewidth=2),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2, color='black'))
            
            ax2.annotate(f'Python {size_labels[s]}\nTempo: {format_time_label(py_time)}\nIter: {format_iter_label(py_iter)}',
                        xy=(py_iter, py_time), xytext=(offset_x_py, offset_y_py),
                        textcoords='offset points', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor=colors_py[s], alpha=0.95, edgecolor='black', linewidth=2),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2, color='black'))
    
    ax2.set_xlabel('Iterações Médias', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Tempo Médio (ms) - Escala Log', fontweight='bold', fontsize=12)
    ax2.set_title('Tempo vs Iterações - Worst Case\nEficiência: Menor tempo para mesma iteração = Mais eficiente', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_yscale('log')
    
    # Adicionar legenda explicativa
    ax2.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_dir / '2_tempo_vs_iteracoes.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 2 salvo: 2_tempo_vs_iteracoes.png")

def plot_summary(df, output_dir):
    """Gráfico 3: Análise de Desempenho - Resumo comparativo (linha)."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    sizes = sorted(df['size'].unique())
    size_labels = {4: '4×4', 9: '9×9', 16: '16×16'}
    
    # Preparar dados para best case
    c_best_times = []
    py_best_times = []
    c_worst_times = []
    py_worst_times = []
    
    for s in sizes:
        c_best = df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]
        py_best = df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]
        c_worst = df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]
        py_worst = df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]
        
        c_best_times.append(c_best['avg_time'].values[0] * 1000 if len(c_best) > 0 else 0)  # Converter para ms
        py_best_times.append(py_best['avg_time'].values[0] * 1000 if len(py_best) > 0 else 0)
        c_worst_times.append(c_worst['avg_time'].values[0] * 1000 if len(c_worst) > 0 else 0)
        py_worst_times.append(py_worst['avg_time'].values[0] * 1000 if len(py_worst) > 0 else 0)
    
    # Plotar linhas
    ax.plot(sizes, c_best_times, marker='s', linestyle='-', linewidth=2, 
            label='C (Compilado) - Best Case', color='#2E86AB', markersize=8)
    ax.plot(sizes, py_best_times, marker='s', linestyle='--', linewidth=2,
            label='Python (Interpretado) - Best Case', color='#A23B72', markersize=8)
    ax.plot(sizes, c_worst_times, marker='o', linestyle='-', linewidth=2,
            label='C (Compilado) - Worst Case', color='#06A77D', markersize=8)
    ax.plot(sizes, py_worst_times, marker='o', linestyle='--', linewidth=2,
            label='Python (Interpretado) - Worst Case', color='#F18F01', markersize=8)
    
    ax.set_xlabel('Tamanho do Sudoku (n×n)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Tempo de Execução (ms) - Escala Log', fontweight='bold', fontsize=11)
    ax.set_title('Análise de Desempenho: Backtracking Iterativo (Python vs C)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(sizes)
    ax.set_xticklabels([size_labels[s] for s in sizes])
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, which='both')
    ax.legend(loc='upper left', fontsize=9)
    
    # Função para formatar tempo similar ao gráfico do heapsort
    def format_time_ms(value):
        """Formata tempo em ms com precisão similar ao gráfico do heapsort."""
        if value <= 0:
            return "0.0"
        # Para valores muito pequenos (< 0.01ms), usar mais casas decimais
        if value < 0.01:
            # Formatar com até 4 casas decimais para valores muito pequenos
            return f'{value:.4f}'.rstrip('0').rstrip('.')
        # Para valores pequenos (< 0.1ms), usar 3 casas decimais
        elif value < 0.1:
            return f'{value:.3f}'.rstrip('0').rstrip('.')
        # Para valores >= 0.1ms, usar 1 casa decimal (como no heapsort: 0.7ms, 21.9ms, etc)
        else:
            return f'{value:.1f}'
    
    # Adicionar valores nos pontos com offset para não ficarem escondidos
    for i, s in enumerate(sizes):
        # Calcular offset baseado no valor (em escala log)
        def get_offset(value):
            """Retorna offset proporcional ao valor para evitar sobreposição."""
            if value <= 0:
                return 0
            # Para escala log, usar offset adaptativo
            # Para valores pequenos, usar porcentagem maior
            # Para valores grandes, usar porcentagem menor para não ficar muito longe
            if value < 0.1:
                return value * 0.2  # 20% para valores muito pequenos
            elif value < 1:
                return value * 0.15  # 15% para valores pequenos
            elif value < 10:
                return value * 0.1  # 10% para valores médios
            else:
                return value * 0.05  # 5% para valores grandes (evita ficar muito longe)
        
        # Best Case - posicionar acima
        if c_best_times[i] > 0:
            offset = get_offset(c_best_times[i])
            ax.text(s, c_best_times[i] * (1 + offset), format_time_ms(c_best_times[i]),
                   ha='center', va='bottom', fontsize=8, color='#2E86AB', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))
        
        if py_best_times[i] > 0:
            offset = get_offset(py_best_times[i])
            ax.text(s, py_best_times[i] * (1 + offset), format_time_ms(py_best_times[i]),
                   ha='center', va='bottom', fontsize=8, color='#A23B72',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Worst Case - posicionar acima também, mas com offset maior se necessário
        if c_worst_times[i] > 0:
            offset = get_offset(c_worst_times[i])
            ax.text(s, c_worst_times[i] * (1 + offset), format_time_ms(c_worst_times[i]),
                   ha='center', va='bottom', fontsize=8, color='#06A77D',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))
        
        if py_worst_times[i] > 0:
            offset = get_offset(py_worst_times[i])
            ax.text(s, py_worst_times[i] * (1 + offset), format_time_ms(py_worst_times[i]),
                   ha='center', va='bottom', fontsize=8, color='#F18F01',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.tight_layout()
    plt.savefig(output_dir / '4_resumo_desempenho.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 4 salvo: 4_resumo_desempenho.png")

def plot_best_vs_worst(df, output_dir):
    """Gráfico 3: Comparação Best vs Worst Case."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    sizes = sorted(df['size'].unique())
    size_labels = {4: 'Small (4×4)', 9: 'Medium (9×9)', 16: 'Large (16×16)'}
    
    # Tempo - separado por linguagem (porque os tempos são diferentes)
    ax1 = axes[0]
    x = np.arange(len(sizes))
    width = 0.2
    
    c_best = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]['avg_time'].values[0] 
              if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]) > 0 else 0 
              for s in sizes]
    c_worst = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]['avg_time'].values[0] 
               if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]) > 0 else 0 
               for s in sizes]
    py_best = [df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]['avg_time'].values[0] 
               if len(df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'best')]) > 0 else 0 
               for s in sizes]
    py_worst = [df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]['avg_time'].values[0] 
                if len(df[(df['lang'] == 'python') & (df['size'] == s) & (df['case'] == 'worst')]) > 0 else 0 
                for s in sizes]
    
    bars1_time = ax1.bar(x - 1.5*width, c_best, width, label='C - Best', color='#2E86AB', alpha=0.8)
    bars2_time = ax1.bar(x - 0.5*width, c_worst, width, label='C - Worst', color='#A23B72', alpha=0.8)
    bars3_time = ax1.bar(x + 0.5*width, py_best, width, label='Python - Best', color='#06A77D', alpha=0.8)
    bars4_time = ax1.bar(x + 1.5*width, py_worst, width, label='Python - Worst', color='#F18F01', alpha=0.8)
    
    ax1.set_xlabel('Tamanho do Sudoku', fontweight='bold')
    ax1.set_ylabel('Tempo Médio (segundos)', fontweight='bold')
    ax1.set_title('Best vs Worst Case - Tempo', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([size_labels[s] for s in sizes])
    ax1.legend()
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras de tempo
    for bars, values in [(bars1_time, c_best), (bars2_time, c_worst), (bars3_time, py_best), (bars4_time, py_worst)]:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        format_time_ms_only(height),
                        ha='center', va='bottom', fontsize=7,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Iterações - NÃO separado por linguagem (porque são iguais)
    ax2 = axes[1]
    width_iter = 0.35  # Barras mais largas já que são apenas 2 por tamanho
    
    # Usar apenas dados de C (ou Python, tanto faz, são iguais)
    best_iter = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]['avg_iterations'].values[0] 
                 if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'best')]) > 0 else 0 
                 for s in sizes]
    worst_iter = [df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]['avg_iterations'].values[0] 
                  if len(df[(df['lang'] == 'c') & (df['size'] == s) & (df['case'] == 'worst')]) > 0 else 0 
                  for s in sizes]
    
    bars1_iter = ax2.bar(x - width_iter/2, best_iter, width_iter, label='Best Case', color='#2E86AB', alpha=0.8)
    bars2_iter = ax2.bar(x + width_iter/2, worst_iter, width_iter, label='Worst Case', color='#A23B72', alpha=0.8)
    
    ax2.set_xlabel('Tamanho do Sudoku', fontweight='bold')
    ax2.set_ylabel('Iterações Médias', fontweight='bold')
    ax2.set_title('Best vs Worst Case - Iterações\n(Valores iguais para C e Python - puzzles idênticos)', 
                  fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([size_labels[s] for s in sizes])
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras de iterações
    for bars, values in [(bars1_iter, best_iter), (bars2_iter, worst_iter)]:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                # Formatar iterações de forma legível
                if height < 1:
                    iter_text = f'{height:.2f}'
                elif height < 1000:
                    iter_text = f'{int(height)}'
                else:
                    iter_text = f'{int(height/1000)}k' if height < 1000000 else f'{int(height/1000000)}M'
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        iter_text,
                        ha='center', va='bottom', fontsize=8, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='black', linewidth=1))
    
    plt.tight_layout()
    plt.savefig(output_dir / '3_best_vs_worst.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 3 salvo: 3_best_vs_worst.png")

def main():
    # Diretórios
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    logs_dir = project_root / 'logs'
    output_dir = script_dir
    
    if not logs_dir.exists():
        print("❌ Diretório 'logs/' não encontrado!")
        print("Execute 'make run-all' para gerar os logs primeiro.")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("📊 GERANDO GRÁFICOS DE PERFORMANCE")
    print("="*80)
    print(f"\n📁 Lendo logs de: {logs_dir}")
    print(f"📁 Salvando gráficos em: {output_dir}\n")
    
    # Carregar dados
    df = load_data(logs_dir)
    
    if df is None or len(df) == 0:
        print("❌ Nenhum dado encontrado nos logs!")
        print("Execute 'make run-all' para gerar os logs primeiro.")
        sys.exit(1)
    
    print(f"✓ {len(df)} configurações carregadas\n")
    
    # Gerar gráficos
    print("Gerando gráficos...\n")
    plot_time_comparison(df, output_dir)
    plot_time_vs_iterations(df, output_dir)
    plot_best_vs_worst(df, output_dir)
    plot_summary(df, output_dir)
    
    print("\n" + "="*80)
    print("✅ Todos os gráficos foram gerados com sucesso!")
    print("="*80)
    print(f"\n📊 Gráficos salvos em: {output_dir}")
    print("\nGráficos gerados:")
    print("  1. 1_tempo_comparacao.png - Comparação de tempo C vs Python")
    print("  2. 2_tempo_vs_iteracoes.png - Tempo vs Iterações (Eficiência)")
    print("  3. 3_best_vs_worst.png - Comparação Best vs Worst Case")
    print("  4. 4_resumo_desempenho.png - Análise de desempenho (resumo)\n")

if __name__ == "__main__":
    main()

