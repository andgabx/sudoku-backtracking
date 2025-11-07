#!/usr/bin/env python3
"""
Script para análise e visualização dos resultados dos testes
Extrai estatísticas dos arquivos de log e gera tabelas comparativas
"""

import os
import re
from pathlib import Path

def parse_log_file(filename):
    """
    Extrai informações de um arquivo de log
    
    Returns:
        dict com estatísticas
    """
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extrai informações usando regex
    lang_match = re.search(r'Linguagem: (\w+)', content)
    size_match = re.search(r'Tamanho: (\d+)x\d+', content)
    case_match = re.search(r'Caso: (\w+)', content)
    success_match = re.search(r'Resoluções bem-sucedidas: (\d+)/(\d+)', content)
    avg_time_match = re.search(r'Tempo médio: ([\d.]+) segundos', content)
    total_time_match = re.search(r'Tempo total: ([\d.]+) segundos', content)
    avg_iter_match = re.search(r'Iterações médias: ([\d.]+)', content)
    total_iter_match = re.search(r'Iterações totais: (\d+)', content)
    
    return {
        'language': lang_match.group(1) if lang_match else 'N/A',
        'size': size_match.group(1) if size_match else 'N/A',
        'case': case_match.group(1) if case_match else 'N/A',
        'successful': int(success_match.group(1)) if success_match else 0,
        'total_runs': int(success_match.group(2)) if success_match else 0,
        'avg_time': float(avg_time_match.group(1)) if avg_time_match else 0.0,
        'total_time': float(total_time_match.group(1)) if total_time_match else 0.0,
        'avg_iterations': float(avg_iter_match.group(1)) if avg_iter_match else 0.0,
        'total_iterations': int(total_iter_match.group(1)) if total_iter_match else 0
    }

def main():
    logs_dir = Path('logs')
    
    if not logs_dir.exists():
        print("❌ Diretório 'logs/' não encontrado!")
        print("Execute 'make run-all' para gerar os logs primeiro.")
        return
    
    # Define ordem dos resultados
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
            results.append(data)
    
    if not results:
        print("❌ Nenhum log encontrado!")
        print("Execute 'make run-all' para gerar os logs primeiro.")
        return
    
    # Exibe resultados
    print("\n" + "="*100)
    print("📊 ANÁLISE DE COMPLEXIDADE - BACKTRACKING ITERATIVO PARA SUDOKU")
    print("="*100)
    
    # Tabela principal
    print("\n{:<10} {:<8} {:<8} {:<12} {:<18} {:<18} {:<10}".format(
        "Linguagem", "Tamanho", "Caso", "Resolvidos", "Tempo Médio (s)", "Iterações Médias", "Sucesso"
    ))
    print("-"*100)
    
    for r in results:
        print("{:<10} {:<8} {:<8} {:<12} {:<18.6f} {:<18.2f} {:<10}".format(
            r['language'],
            r['size'] + 'x' + r['size'],
            r['case'],
            f"{r['successful']}/{r['total_runs']}",
            r['avg_time'],
            r['avg_iterations'],
            "✓" if r['successful'] == r['total_runs'] else "✗"
        ))
    
    # Análise comparativa C vs Python
    print("\n" + "="*100)
    print("📈 ANÁLISE COMPARATIVA: C vs PYTHON")
    print("="*100)
    
    # Agrupa por size_case
    size_case_map = {}
    for r in results:
        key = f"{r['size']}_{r['case']}"
        if key not in size_case_map:
            size_case_map[key] = []
        size_case_map[key].append(r)
    
    print("\n{:<15} {:<15} {:<15} {:<20}".format(
        "Configuração", "C (segundos)", "Python (seg)", "Speedup (C vs Py)"
    ))
    print("-"*100)
    
    for key, data in size_case_map.items():
        if len(data) == 2:
            c_data = next((d for d in data if d['language'] == 'C'), None)
            py_data = next((d for d in data if d['language'] == 'Python'), None)
            
            if c_data and py_data and c_data['avg_time'] > 0:
                speedup = py_data['avg_time'] / c_data['avg_time']
                print("{:<15} {:<15.6f} {:<15.6f} {:<20.2f}x".format(
                    key.replace('_', ' ').title(),
                    c_data['avg_time'],
                    py_data['avg_time'],
                    speedup
                ))
    
    # Resumo de complexidade
    print("\n" + "="*100)
    print("🔬 ANÁLISE DE COMPLEXIDADE")
    print("="*100)
    print("\nObservações sobre a complexidade de tempo:\n")
    
    # Compara best vs worst para cada tamanho
    sizes_found = {}
    for r in results:
        if r['language'] == 'C':  # Usa C como referência
            key = (r['size'], r['case'])
            sizes_found[key] = r
    
    # Agrupa por tamanho
    size_groups = {}
    for (size, case), r in sizes_found.items():
        if size not in size_groups:
            size_groups[size] = {}
        size_groups[size][case] = r
    
    for size, cases in sorted(size_groups.items()):
        if 'best' in cases and 'worst' in cases:
            best = cases['best']
            worst = cases['worst']
            ratio = worst['avg_iterations'] / best['avg_iterations'] if best['avg_iterations'] > 0 else 0
            print(f"• Tamanho {size}x{size}:")
            print(f"  - Best Case:  {best['avg_iterations']:.2f} iterações médias")
            print(f"  - Worst Case: {worst['avg_iterations']:.2f} iterações médias")
            print(f"  - Razão:      {ratio:.2f}x mais iterações no pior caso\n")
    
    print("\n" + "="*100)
    print("✅ Análise concluída!")
    print("="*100)
    print("\n💡 Dica: Use esses dados para criar gráficos no seu relatório!")
    print("   Os arquivos de log completos estão em: logs/\n")

if __name__ == "__main__":
    main()
