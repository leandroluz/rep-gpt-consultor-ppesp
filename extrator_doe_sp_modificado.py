#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extrator de Legislação da Polícia Penal de SP do Diário Oficial
Este script extrai decretos, resoluções e portarias relacionados à Polícia Penal
do Diário Oficial do Estado de São Paulo dos últimos 3 anos.
"""

import os
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class ExtratorDOESP:
    def __init__(self, diretorio_saida="./dados"):
        """
        Inicializa o extrator do Diário Oficial de SP
        
        Args:
            diretorio_saida: Diretório onde os arquivos extraídos serão salvos
        """
        self.url_base = "https://www.doe.sp.gov.br/"
        self.diretorio_saida = diretorio_saida
        self.driver = None
        
        # Criar diretórios para armazenar os dados organizados por data (ano/mês)
        os.makedirs(self.diretorio_saida, exist_ok=True)
        os.makedirs(os.path.join(self.diretorio_saida, "metadados"), exist_ok=True)
        
        # Criar diretórios para os últimos 3 anos
        hoje = datetime.datetime.now()
        for i in range(3):
            ano = hoje.year - i
            for mes in range(1, 13):
                os.makedirs(os.path.join(self.diretorio_saida, str(ano), f"{mes:02d}"), exist_ok=True)
        
    def iniciar_navegador(self):
        """Inicializa o navegador Chrome em modo headless"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
    def fechar_navegador(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            
    def calcular_data_inicio(self, anos=3):
        """
        Calcula a data de início para a busca (X anos atrás)
        
        Args:
            anos: Número de anos para retroceder
            
        Returns:
            data_inicio: Data de início no formato DD/MM/AAAA
        """
        hoje = datetime.datetime.now()
        data_inicio = hoje - datetime.timedelta(days=365 * anos)
        return data_inicio.strftime("%d/%m/%Y")
    
    def buscar_legislacao(self, termo, tipo_documento, data_inicio, data_fim=None):
        """
        Realiza busca de legislação no Diário Oficial
        
        Args:
            termo: Termo de busca (ex: "polícia penal")
            tipo_documento: Tipo de documento a ser buscado (decreto, resolucao, portaria)
            data_inicio: Data de início no formato DD/MM/AAAA
            data_fim: Data de fim no formato DD/MM/AAAA (opcional, padrão é a data atual)
            
        Returns:
            resultados: Lista de dicionários com os resultados encontrados
        """
        if not self.driver:
            self.iniciar_navegador()
            
        if not data_fim:
            data_fim = datetime.datetime.now().strftime("%d/%m/%Y")
            
        # Navegar para a página de busca
        self.driver.get(self.url_base)
        
        try:
            # Preencher o campo de busca
            campo_busca = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar por termo no dia de hoje']"))
            )
            campo_busca.clear()
            campo_busca.send_keys(f"{termo} {tipo_documento}")
            
            # Clicar no botão de busca avançada
            botao_busca_avancada = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'search-advanced')]"))
            )
            botao_busca_avancada.click()
            
            # Selecionar opção de período personalizado
            seletor_data = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Hoje']"))
            )
            seletor_data.click()
            
            # Preencher data de início
            campo_data_inicio = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='DD/MM/AAAA'][1]"))
            )
            campo_data_inicio.clear()
            campo_data_inicio.send_keys(data_inicio)
            
            # Preencher data de fim
            campo_data_fim = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='DD/MM/AAAA'][2]"))
            )
            campo_data_fim.clear()
            campo_data_fim.send_keys(data_fim)
            
            # Selecionar caderno Executivo
            seletor_caderno = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Todos']"))
            )
            seletor_caderno.click()
            
            opcao_executivo = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[text()='Executivo']"))
            )
            opcao_executivo.click()
            
            # Clicar no botão de pesquisar
            botao_pesquisar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='PESQUISAR']"))
            )
            botao_pesquisar.click()
            
            # Aguardar os resultados
            time.sleep(5)
            
            # Extrair resultados
            resultados = []
            pagina_atual = 1
            
            while True:
                # Extrair resultados da página atual
                itens_resultado = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'result-item')]"))
                )
                
                for item in itens_resultado:
                    try:
                        titulo = item.find_element(By.XPATH, ".//h2").text
                        data_publicacao = item.find_element(By.XPATH, ".//span[contains(text(), 'PUBLICADO EM:')]").text
                        data_publicacao = data_publicacao.replace("PUBLICADO EM:", "").strip()
                        
                        # Clicar no botão "VER PUBLICAÇÃO" para acessar o conteúdo
                        botao_ver = item.find_element(By.XPATH, ".//button[text()='VER PUBLICAÇÃO']")
                        botao_ver.click()
                        
                        # Aguardar carregamento do conteúdo
                        time.sleep(3)
                        
                        # Extrair o conteúdo completo
                        conteudo = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'publication-content')]"))
                        ).text
                        
                        # Voltar para a lista de resultados
                        botao_voltar = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'back-button')]"))
                        )
                        botao_voltar.click()
                        
                        # Aguardar retorno à lista
                        time.sleep(2)
                        
                        # Adicionar resultado à lista
                        resultados.append({
                            "titulo": titulo,
                            "data_publicacao": data_publicacao,
                            "conteudo": conteudo,
                            "tipo": tipo_documento
                        })
                        
                    except Exception as e:
                        print(f"Erro ao processar item: {str(e)}")
                        continue
                
                # Verificar se há mais páginas
                try:
                    pagina_atual += 1
                    botao_proxima = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[text()='{pagina_atual}']"))
                    )
                    botao_proxima.click()
                    time.sleep(3)
                except (TimeoutException, NoSuchElementException):
                    # Não há mais páginas
                    break
            
            return resultados
            
        except Exception as e:
            print(f"Erro durante a busca: {str(e)}")
            return []
    
    def salvar_resultado(self, resultado):
        """
        Salva um resultado em arquivo, organizado por data
        
        Args:
            resultado: Dicionário com os dados do resultado
        """
        tipo = resultado["tipo"]
        data_str = resultado["data_publicacao"]
        titulo = resultado["titulo"]
        
        # Converter data para objeto datetime
        try:
            data = datetime.datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            # Se o formato da data for diferente, usar a data atual
            data = datetime.datetime.now()
            
        ano = data.year
        mes = data.month
        
        # Criar nome de arquivo seguro
        nome_arquivo_base = titulo.lower()
        nome_arquivo_base = ''.join(c if c.isalnum() else '_' for c in nome_arquivo_base)
        nome_arquivo = f"{data.strftime('%Y-%m-%d')}_{tipo.lower()}_{nome_arquivo_base}"
        
        # Determinar diretório de saída com base na data
        diretorio = os.path.join(self.diretorio_saida, str(ano), f"{mes:02d}")
        os.makedirs(diretorio, exist_ok=True)
        
        # Salvar conteúdo em arquivo de texto
        caminho_arquivo_txt = os.path.join(diretorio, f"{nome_arquivo}.txt")
        with open(caminho_arquivo_txt, 'w', encoding='utf-8') as f:
            f.write(f"Título: {resultado['titulo']}\n")
            f.write(f"Data de Publicação: {resultado['data_publicacao']}\n")
            f.write(f"Tipo: {resultado['tipo']}\n")
            f.write("\n--- CONTEÚDO ---\n\n")
            f.write(resultado['conteudo'])
        
        # Salvar metadados em JSON
        metadados = {
            "titulo": resultado['titulo'],
            "data_publicacao": resultado['data_publicacao'],
            "tipo": resultado['tipo'],
            "arquivo_texto": caminho_arquivo_txt
        }
        
        caminho_arquivo_json = os.path.join(self.diretorio_saida, "metadados", f"{nome_arquivo}.json")
        with open(caminho_arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(metadados, f, ensure_ascii=False, indent=4)
            
        return {
            "arquivo_texto": caminho_arquivo_txt,
            "arquivo_json": caminho_arquivo_json
        }
    
    def extrair_legislacao_policia_penal(self, anos=3):
        """
        Extrai toda a legislação relacionada à Polícia Penal dos últimos X anos
        
        Args:
            anos: Número de anos para retroceder na busca
            
        Returns:
            resultados: Dicionário com os resultados por tipo de documento
        """
        try:
            self.iniciar_navegador()
            
            data_inicio = self.calcular_data_inicio(anos)
            resultados_totais = {
                "decretos": [],
                "resolucoes": [],
                "portarias": []
            }
            
            # Buscar decretos
            print("Buscando decretos relacionados à Polícia Penal...")
            decretos = self.buscar_legislacao("polícia penal", "decreto", data_inicio)
            for decreto in decretos:
                arquivos = self.salvar_resultado(decreto)
                resultados_totais["decretos"].append({
                    "titulo": decreto["titulo"],
                    "data": decreto["data_publicacao"],
                    "arquivos": arquivos
                })
            
            # Buscar resoluções
            print("Buscando resoluções relacionadas à Polícia Penal...")
            resolucoes = self.buscar_legislacao("polícia penal", "resolução", data_inicio)
            for resolucao in resolucoes:
                arquivos = self.salvar_resultado(resolucao)
                resultados_totais["resolucoes"].append({
                    "titulo": resolucao["titulo"],
                    "data": resolucao["data_publicacao"],
                    "arquivos": arquivos
                })
            
            # Buscar portarias
            print("Buscando portarias relacionadas à Polícia Penal...")
            portarias = self.buscar_legislacao("polícia penal", "portaria", data_inicio)
            for portaria in portarias:
                arquivos = self.salvar_resultado(portaria)
                resultados_totais["portarias"].append({
                    "titulo": portaria["titulo"],
                    "data": portaria["data_publicacao"],
                    "arquivos": arquivos
                })
            
            # Salvar resumo dos resultados
            resumo = {
                "data_extracao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "periodo_busca": {
                    "inicio": data_inicio,
                    "fim": datetime.datetime.now().strftime("%d/%m/%Y")
                },
                "quantidade": {
                    "decretos": len(resultados_totais["decretos"]),
                    "resolucoes": len(resultados_totais["resolucoes"]),
                    "portarias": len(resultados_totais["portarias"]),
                    "total": len(decretos) + len(resolucoes) + len(portarias)
                },
                "resultados": resultados_totais
            }
            
            with open(os.path.join(self.diretorio_saida, "resumo_extracao.json"), 'w', encoding='utf-8') as f:
                json.dump(resumo, f, ensure_ascii=False, indent=4)
                
            return resumo
            
        except Exception as e:
            print(f"Erro durante a extração: {str(e)}")
            return None
        finally:
            self.fechar_navegador()

def main():
    """Função principal"""
    diretorio_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
    extrator = ExtratorDOESP(diretorio_saida)
    
    print("Iniciando extração de legislação da Polícia Penal de SP...")
    resumo = extrator.extrair_legislacao_policia_penal(anos=3)
    
    if resumo:
        print("\nExtração concluída com sucesso!")
        print(f"Total de documentos extraídos: {resumo['quantidade']['total']}")
        print(f"- Decretos: {resumo['quantidade']['decretos']}")
        print(f"- Resoluções: {resumo['quantidade']['resolucoes']}")
        print(f"- Portarias: {resumo['quantidade']['portarias']}")
        print(f"\nOs arquivos foram salvos em: {diretorio_saida}")
    else:
        print("Falha na extração de legislação.")

if __name__ == "__main__":
    main()
