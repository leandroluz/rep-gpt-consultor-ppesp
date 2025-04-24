#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Índice para Repositório de Legislação da Polícia Penal de SP
Este script gera um arquivo index.html para facilitar a navegação no repositório.
"""

import os
import json
import datetime

def gerar_index_html(diretorio_dados, diretorio_saida):
    """
    Gera um arquivo index.html para o repositório
    
    Args:
        diretorio_dados: Diretório onde os dados estão armazenados
        diretorio_saida: Diretório onde o arquivo index.html será salvo
    """
    # Verificar se o resumo da extração existe
    caminho_resumo = os.path.join(diretorio_dados, "resumo_extracao.json")
    if not os.path.exists(caminho_resumo):
        print("Arquivo de resumo não encontrado. Execute a extração primeiro.")
        return False
    
    # Carregar dados do resumo
    with open(caminho_resumo, 'r', encoding='utf-8') as f:
        resumo = json.load(f)
    
    # Coletar informações dos documentos
    decretos = []
    resolucoes = []
    portarias = []
    
    # Diretório de decretos
    dir_decretos = os.path.join(diretorio_dados, "decretos")
    if os.path.exists(dir_decretos):
        for arquivo in os.listdir(dir_decretos):
            if arquivo.endswith(".txt"):
                caminho = os.path.join(dir_decretos, arquivo)
                with open(caminho, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    titulo = linhas[0].replace("Título: ", "").strip()
                    data = linhas[1].replace("Data de Publicação: ", "").strip()
                    decretos.append({
                        "titulo": titulo,
                        "data": data,
                        "arquivo": os.path.basename(caminho)
                    })
    
    # Diretório de resoluções
    dir_resolucoes = os.path.join(diretorio_dados, "resolucoes")
    if os.path.exists(dir_resolucoes):
        for arquivo in os.listdir(dir_resolucoes):
            if arquivo.endswith(".txt"):
                caminho = os.path.join(dir_resolucoes, arquivo)
                with open(caminho, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    titulo = linhas[0].replace("Título: ", "").strip()
                    data = linhas[1].replace("Data de Publicação: ", "").strip()
                    resolucoes.append({
                        "titulo": titulo,
                        "data": data,
                        "arquivo": os.path.basename(caminho)
                    })
    
    # Diretório de portarias
    dir_portarias = os.path.join(diretorio_dados, "portarias")
    if os.path.exists(dir_portarias):
        for arquivo in os.listdir(dir_portarias):
            if arquivo.endswith(".txt"):
                caminho = os.path.join(dir_portarias, arquivo)
                with open(caminho, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    titulo = linhas[0].replace("Título: ", "").strip()
                    data = linhas[1].replace("Data de Publicação: ", "").strip()
                    portarias.append({
                        "titulo": titulo,
                        "data": data,
                        "arquivo": os.path.basename(caminho)
                    })
    
    # Ordenar por data (mais recente primeiro)
    decretos.sort(key=lambda x: x["data"], reverse=True)
    resolucoes.sort(key=lambda x: x["data"], reverse=True)
    portarias.sort(key=lambda x: x["data"], reverse=True)
    
    # Gerar HTML
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repositório de Legislação da Polícia Penal de SP</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background-color: #1a5276;
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        h1 {{
            margin: 0;
        }}
        h2 {{
            color: #1a5276;
            border-bottom: 2px solid #1a5276;
            padding-bottom: 5px;
        }}
        .info-box {{
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .tab {{
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            border-radius: 5px 5px 0 0;
        }}
        .tab button {{
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 16px;
        }}
        .tab button:hover {{
            background-color: #ddd;
        }}
        .tab button.active {{
            background-color: #1a5276;
            color: white;
        }}
        .tabcontent {{
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .search-container {{
            margin-bottom: 20px;
        }}
        .search-container input {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Repositório de Legislação da Polícia Penal de SP</h1>
            <p>Decretos, Resoluções e Portarias dos últimos 3 anos</p>
        </header>
        
        <div class="info-box">
            <h3>Informações da Extração</h3>
            <p><strong>Data da extração:</strong> {resumo['data_extracao']}</p>
            <p><strong>Período:</strong> {resumo['periodo_busca']['inicio']} a {resumo['periodo_busca']['fim']}</p>
            <p><strong>Total de documentos:</strong> {resumo['quantidade']['total']}</p>
            <ul>
                <li><strong>Decretos:</strong> {resumo['quantidade']['decretos']}</li>
                <li><strong>Resoluções:</strong> {resumo['quantidade']['resolucoes']}</li>
                <li><strong>Portarias:</strong> {resumo['quantidade']['portarias']}</li>
            </ul>
        </div>
        
        <div class="search-container">
            <input type="text" id="searchInput" onkeyup="searchDocuments()" placeholder="Pesquisar em todos os documentos...">
        </div>
        
        <div class="tab">
            <button class="tablinks active" onclick="openTab(event, 'Decretos')">Decretos</button>
            <button class="tablinks" onclick="openTab(event, 'Resolucoes')">Resoluções</button>
            <button class="tablinks" onclick="openTab(event, 'Portarias')">Portarias</button>
        </div>
        
        <div id="Decretos" class="tabcontent" style="display: block;">
            <h2>Decretos</h2>
            <table id="tabelaDecretos">
                <tr>
                    <th>Título</th>
                    <th>Data de Publicação</th>
                    <th>Ações</th>
                </tr>
"""
    
    # Adicionar decretos
    for decreto in decretos:
        html += f"""                <tr>
                    <td>{decreto['titulo']}</td>
                    <td>{decreto['data']}</td>
                    <td><a href="decretos/{decreto['arquivo']}" target="_blank">Ver Documento</a></td>
                </tr>
"""
    
    html += """            </table>
        </div>
        
        <div id="Resolucoes" class="tabcontent">
            <h2>Resoluções</h2>
            <table id="tabelaResolucoes">
                <tr>
                    <th>Título</th>
                    <th>Data de Publicação</th>
                    <th>Ações</th>
                </tr>
"""
    
    # Adicionar resoluções
    for resolucao in resolucoes:
        html += f"""                <tr>
                    <td>{resolucao['titulo']}</td>
                    <td>{resolucao['data']}</td>
                    <td><a href="resolucoes/{resolucao['arquivo']}" target="_blank">Ver Documento</a></td>
                </tr>
"""
    
    html += """            </table>
        </div>
        
        <div id="Portarias" class="tabcontent">
            <h2>Portarias</h2>
            <table id="tabelaPortarias">
                <tr>
                    <th>Título</th>
                    <th>Data de Publicação</th>
                    <th>Ações</th>
                </tr>
"""
    
    # Adicionar portarias
    for portaria in portarias:
        html += f"""                <tr>
                    <td>{portaria['titulo']}</td>
                    <td>{portaria['data']}</td>
                    <td><a href="portarias/{portaria['arquivo']}" target="_blank">Ver Documento</a></td>
                </tr>
"""
    
    html += """            </table>
        </div>
        
        <footer>
            <p>Repositório de Legislação da Polícia Penal de SP - Atualizado em """ + datetime.datetime.now().strftime("%d/%m/%Y") + """</p>
        </footer>
    </div>
    
    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        function searchDocuments() {
            var input, filter, tables, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            tables = ["tabelaDecretos", "tabelaResolucoes", "tabelaPortarias"];
            
            for (j = 0; j < tables.length; j++) {
                table = document.getElementById(tables[j]);
                tr = table.getElementsByTagName("tr");
                
                for (i = 1; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[0]; // Título
                    if (td) {
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        } else {
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
        }
    </script>
</body>
</html>
"""
    
    # Salvar o arquivo HTML
    caminho_index = os.path.join(diretorio_saida, "index.html")
    with open(caminho_index, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Arquivo index.html gerado com sucesso em: {caminho_index}")
    return True

def main():
    """Função principal"""
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    diretorio_dados = os.path.join(diretorio_base, "dados")
    
    print("Gerando arquivo index.html para o repositório...")
    sucesso = gerar_index_html(diretorio_dados, diretorio_dados)
    
    if sucesso:
        print("Geração do index.html concluída com sucesso!")
    else:
        print("Falha na geração do index.html.")

if __name__ == "__main__":
    main()
