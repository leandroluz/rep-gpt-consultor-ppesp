#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Atualização Manual para o Repositório de Legislação da Polícia Penal de SP
Este script permite adicionar novos documentos ao repositório de forma manual.
"""

import os
import sys
import re
import datetime
import shutil
from pathlib import Path

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Exibe o cabeçalho do sistema"""
    print("=" * 80)
    print("SISTEMA DE ATUALIZAÇÃO DO REPOSITÓRIO DE LEGISLAÇÃO DA POLÍCIA PENAL DE SP")
    print("=" * 80)
    print()

def validate_date(date_str):
    """Valida se a string está no formato de data DD/MM/AAAA"""
    try:
        datetime.datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def create_safe_filename(title, date_str, doc_type):
    """Cria um nome de arquivo seguro baseado no título, data e tipo do documento"""
    # Converter data para formato YYYY-MM-DD
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    
    # Extrair número do documento se existir
    num_match = re.search(r'[Nn][º°]\s*(\d+[\.\d]*)', title)
    if num_match:
        doc_num = num_match.group(1)
    else:
        # Extrair números de resolução/portaria se existir
        num_match = re.search(r'([A-Za-z]+)[- ](\d+)', title)
        if num_match:
            doc_num = f"{num_match.group(1).lower()}_{num_match.group(2)}"
        else:
            # Usar parte do título se não houver número
            words = re.sub(r'[^\w\s]', '', title.lower()).split()
            doc_num = '_'.join(words[:3]) if words else 'documento'
    
    # Criar nome do arquivo
    filename = f"{formatted_date}_{doc_type.lower()}_{doc_num}.txt"
    
    # Substituir caracteres inválidos
    filename = re.sub(r'[^\w\-\.]', '_', filename)
    
    return filename

def add_document():
    """Adiciona um novo documento ao repositório"""
    clear_screen()
    print_header()
    print("ADICIONAR NOVO DOCUMENTO")
    print("-" * 40)
    
    # Solicitar informações do documento
    print("Tipo de documento:")
    print("1. Decreto")
    print("2. Resolução")
    print("3. Portaria")
    
    while True:
        try:
            tipo_opcao = int(input("\nEscolha o tipo (1-3): "))
            if 1 <= tipo_opcao <= 3:
                break
            print("Opção inválida. Escolha entre 1 e 3.")
        except ValueError:
            print("Por favor, digite um número.")
    
    tipos = {1: "Decreto", 2: "Resolução", 3: "Portaria"}
    tipo_documento = tipos[tipo_opcao]
    
    titulo = input("\nTítulo do documento: ")
    
    while True:
        data_publicacao = input("\nData de publicação (DD/MM/AAAA): ")
        if validate_date(data_publicacao):
            break
        print("Formato de data inválido. Use DD/MM/AAAA.")
    
    print("\nConteúdo do documento (digite 'FIM' em uma linha separada para terminar):")
    linhas_conteudo = []
    while True:
        linha = input()
        if linha == "FIM":
            break
        linhas_conteudo.append(linha)
    
    conteudo = "\n".join(linhas_conteudo)
    
    # Criar estrutura do documento
    documento = f"Título: {titulo}\n"
    documento += f"Data de Publicação: {data_publicacao}\n"
    documento += f"Tipo: {tipo_documento}\n"
    documento += "\n--- CONTEÚDO ---\n\n"
    documento += conteudo
    
    # Determinar o diretório de destino
    data_obj = datetime.datetime.strptime(data_publicacao, "%d/%m/%Y")
    ano = data_obj.year
    mes = data_obj.month
    
    diretorio_destino = os.path.join("site", str(ano), f"{mes:02d}")
    
    # Verificar se o diretório existe, criar se necessário
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
    
    # Criar nome de arquivo
    nome_arquivo = create_safe_filename(titulo, data_publicacao, tipo_documento)
    caminho_arquivo = os.path.join(diretorio_destino, nome_arquivo)
    
    # Salvar o documento
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(documento)
    
    print(f"\nDocumento salvo com sucesso em: {caminho_arquivo}")
    input("\nPressione Enter para continuar...")

def update_index_html():
    """Atualiza o arquivo index.html com os novos documentos"""
    clear_screen()
    print_header()
    print("ATUALIZANDO INTERFACE WEB...")
    
    # Caminho para o diretório do site
    site_dir = "site"
    
    # Coletar todos os documentos
    documentos = []
    
    # Percorrer todos os diretórios de ano
    for ano_dir in sorted(os.listdir(site_dir), reverse=True):
        if not ano_dir.isdigit() or ano_dir == "index.html":
            continue
        
        ano = int(ano_dir)
        
        # Percorrer todos os diretórios de mês
        for mes_dir in sorted(os.listdir(os.path.join(site_dir, ano_dir))):
            if not mes_dir.isdigit():
                continue
            
            mes = int(mes_dir)
            mes_path = os.path.join(site_dir, ano_dir, mes_dir)
            
            # Percorrer todos os arquivos no diretório do mês
            for arquivo in os.listdir(mes_path):
                if not arquivo.endswith('.txt'):
                    continue
                
                arquivo_path = os.path.join(mes_path, arquivo)
                
                # Ler metadados do arquivo
                with open(arquivo_path, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    
                    if len(linhas) >= 3:
                        titulo = linhas[0].replace('Título: ', '').strip()
                        data_pub = linhas[1].replace('Data de Publicação: ', '').strip()
                        tipo = linhas[2].replace('Tipo: ', '').strip().lower()
                        
                        # Extrair descrição curta do título
                        descricao = titulo
                        if ' - ' in titulo:
                            partes = titulo.split(' - ', 1)
                            if len(partes) > 1:
                                descricao = partes[1]
                        
                        # Determinar o caminho relativo
                        caminho_relativo = os.path.join(ano_dir, mes_dir, arquivo)
                        
                        documentos.append({
                            'ano': ano,
                            'mes': mes,
                            'titulo': titulo,
                            'descricao': descricao,
                            'data': data_pub,
                            'tipo': tipo,
                            'arquivo': caminho_relativo
                        })
    
    # Backup do index.html atual
    index_path = os.path.join(site_dir, "index.html")
    if os.path.exists(index_path):
        backup_path = os.path.join(site_dir, "index.html.bak")
        shutil.copy2(index_path, backup_path)
        print(f"Backup do index.html criado em: {backup_path}")
    
    # Gerar conteúdo HTML para cada ano
    anos_unicos = sorted(set(doc['ano'] for doc in documentos), reverse=True)
    
    # Ler o template do index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Para cada ano, atualizar a seção correspondente
    for ano in anos_unicos:
        docs_ano = [doc for doc in documentos if doc['ano'] == ano]
        
        # Agrupar por mês
        meses = {}
        for doc in docs_ano:
            if doc['mes'] not in meses:
                meses[doc['mes']] = []
            meses[doc['mes']].append(doc)
        
        # Gerar HTML para os meses
        meses_html = ""
        for mes in sorted(meses.keys(), reverse=True):
            nome_mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                       "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"][mes-1]
            
            meses_html += f'''
                    <div class="month-card">
                        <div class="month-header">{nome_mes}</div>
                        <div class="document-list">
            '''
            
            if not meses[mes]:
                meses_html += '''
                            <div class="empty-month">Nenhum documento encontrado</div>
                '''
            else:
                for doc in sorted(meses[mes], key=lambda x: x['data'], reverse=True):
                    tipo_class = ""
                    if "decreto" in doc['tipo'].lower():
                        tipo_class = "decreto"
                    elif "resolução" in doc['tipo'].lower() or "resolucao" in doc['tipo'].lower():
                        tipo_class = "resolucao"
                    elif "portaria" in doc['tipo'].lower():
                        tipo_class = "portaria"
                    
                    meses_html += f'''
                            <div class="document-item">
                                <a href="#" onclick="openDocument('{doc['arquivo']}')">
                                    <span class="document-type {tipo_class}">{doc['tipo'].capitalize()}</span>
                                    {doc['descricao']}
                                </a>
                                <div class="document-date">Publicado em: {doc['data']}</div>
                            </div>
                    '''
            
            meses_html += '''
                        </div>
                    </div>
            '''
        
        # Substituir a seção do ano no HTML
        ano_pattern = f'<div id="documents-{ano}" class="documents-container">.*?<h3 class="year-title">Legislação de {ano}</h3>.*?<div class="months-grid">(.*?)</div>\\s*</div>'
        replacement = f'''<div id="documents-{ano}" class="documents-container">
                <h3 class="year-title">Legislação de {ano}</h3>
                <div class="months-grid">{meses_html}
                </div>
            </div>'''
        
        # Usar regex com flag DOTALL para capturar múltiplas linhas
        html_content = re.sub(ano_pattern, replacement, html_content, flags=re.DOTALL)
    
    # Atualizar a data de atualização no rodapé
    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    html_content = re.sub(r'Atualizado em \d{2}/\d{2}/\d{4}', f'Atualizado em {hoje}', html_content)
    
    # Salvar o HTML atualizado
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Interface web atualizada com sucesso!")
    input("\nPressione Enter para continuar...")

def main():
    """Função principal do sistema"""
    while True:
        clear_screen()
        print_header()
        print("MENU PRINCIPAL")
        print("-" * 40)
        print("1. Adicionar novo documento")
        print("2. Atualizar interface web")
        print("3. Sair")
        
        try:
            opcao = int(input("\nEscolha uma opção (1-3): "))
            
            if opcao == 1:
                add_document()
            elif opcao == 2:
                update_index_html()
            elif opcao == 3:
                clear_screen()
                print("Obrigado por usar o Sistema de Atualização do Repositório!")
                sys.exit(0)
            else:
                print("Opção inválida. Escolha entre 1 e 3.")
                input("\nPressione Enter para continuar...")
        except ValueError:
            print("Por favor, digite um número.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    # Verificar se está no diretório correto
    if not os.path.exists("site"):
        print("Erro: Diretório 'site' não encontrado.")
        print("Execute este script no diretório raiz do repositório.")
        sys.exit(1)
    
    main()
