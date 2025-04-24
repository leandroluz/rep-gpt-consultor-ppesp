# Extrator de Legislação da Polícia Penal de SP

Este projeto tem como objetivo extrair e organizar a legislação relacionada à Polícia Penal do Estado de São Paulo publicada no Diário Oficial do Estado (DOE-SP), criando um repositório online acessível que possa ser consultado por sistemas de IA como o ChatGPT.

## Estrutura do Projeto

- `extrator_doe_sp.py`: Script principal para extração de legislação do Diário Oficial
- `dados/`: Diretório onde os documentos extraídos são armazenados
  - `decretos/`: Decretos relacionados à Polícia Penal
  - `resolucoes/`: Resoluções relacionadas à Polícia Penal
  - `portarias/`: Portarias relacionadas à Polícia Penal
  - `metadados/`: Arquivos JSON com metadados dos documentos
- `todo.md`: Lista de tarefas do projeto

## Funcionalidades

O extrator automatiza o processo de:

1. Acessar o site do Diário Oficial de SP (doe.sp.gov.br)
2. Realizar buscas por decretos, resoluções e portarias relacionados à Polícia Penal
3. Filtrar resultados dos últimos 3 anos
4. Extrair o conteúdo completo dos documentos
5. Organizar os documentos em uma estrutura de diretórios por tipo
6. Gerar metadados para facilitar a busca e indexação

## Requisitos

- Python 3.6+
- Bibliotecas: requests, beautifulsoup4, selenium, webdriver-manager

## Como Usar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute o script principal:
   ```
   python extrator_doe_sp.py
   ```

3. Os documentos extraídos serão salvos no diretório `dados/` organizados por tipo.

## Próximos Passos

- Criar um repositório online para hospedar os documentos extraídos
- Implementar um sistema de atualização automática
- Desenvolver uma interface de consulta para facilitar o acesso aos documentos

## Licença

Este projeto é disponibilizado como código aberto sob a licença MIT.
