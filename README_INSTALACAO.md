# Guia de Instalação e Uso do Repositório de Legislação da Polícia Penal de SP

Este documento fornece instruções detalhadas para instalar, configurar e utilizar o Repositório de Legislação da Polícia Penal de SP em um ambiente de produção.

## Requisitos do Sistema

- Servidor web (Apache, Nginx, etc.) ou serviço de hospedagem estática (GitHub Pages, Netlify, Vercel)
- Python 3.6+ (para o script de atualização)
- Acesso SSH ou FTP ao servidor (para transferência de arquivos)

## Estrutura de Arquivos

```
legislacao_ppesp/
├── site/                      # Diretório principal do site
│   ├── index.html             # Página principal do repositório
│   ├── 2022/                  # Legislação de 2022 (organizada por mês)
│   ├── 2023/                  # Legislação de 2023 (organizada por mês)
│   ├── 2024/                  # Legislação de 2024 (organizada por mês)
│   └── 2025/                  # Legislação de 2025 (organizada por mês)
├── atualizar_repositorio.py   # Script para atualização manual do repositório
├── README.md                  # Documentação geral do projeto
└── README_INSTALACAO.md       # Este guia de instalação
```

## Opções de Hospedagem

### 1. Hospedagem em Servidor Web Tradicional

#### Instalação no Apache

1. Transfira todos os arquivos para o diretório do seu servidor web:
   ```bash
   scp -r legislacao_ppesp/* usuario@seu-servidor:/var/www/html/legislacao-ppenal/
   ```

2. Configure o Apache para servir os arquivos estáticos:
   ```apache
   <VirtualHost *:80>
       ServerName legislacao-ppenal.seudominio.com
       DocumentRoot /var/www/html/legislacao-ppenal/site
       
       <Directory /var/www/html/legislacao-ppenal/site>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
       
       ErrorLog ${APACHE_LOG_DIR}/legislacao-ppenal-error.log
       CustomLog ${APACHE_LOG_DIR}/legislacao-ppenal-access.log combined
   </VirtualHost>
   ```

3. Reinicie o Apache:
   ```bash
   sudo systemctl restart apache2
   ```

#### Instalação no Nginx

1. Transfira todos os arquivos para o diretório do seu servidor web:
   ```bash
   scp -r legislacao_ppesp/* usuario@seu-servidor:/var/www/legislacao-ppenal/
   ```

2. Configure o Nginx para servir os arquivos estáticos:
   ```nginx
   server {
       listen 80;
       server_name legislacao-ppenal.seudominio.com;
       root /var/www/legislacao-ppenal/site;
       index index.html;
       
       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

3. Reinicie o Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

### 2. Hospedagem em Plataformas Estáticas

#### GitHub Pages

1. Crie um repositório no GitHub chamado `legislacao-ppenal-sp`

2. Clone o repositório localmente:
   ```bash
   git clone https://github.com/seu-usuario/legislacao-ppenal-sp.git
   cd legislacao-ppenal-sp
   ```

3. Copie os arquivos do diretório `site` para o repositório:
   ```bash
   cp -r /caminho/para/legislacao_ppesp/site/* .
   ```

4. Adicione, faça commit e envie os arquivos para o GitHub:
   ```bash
   git add .
   git commit -m "Adicionando repositório de legislação da Polícia Penal de SP"
   git push origin main
   ```

5. Nas configurações do repositório no GitHub, ative o GitHub Pages e selecione a branch `main` como fonte.

6. O site estará disponível em `https://seu-usuario.github.io/legislacao-ppenal-sp/`

#### Netlify

1. Crie uma conta no Netlify (https://www.netlify.com/)

2. Clique em "New site from Git" e selecione seu repositório GitHub

3. Configure as opções de build:
   - Base directory: `site`
   - Publish directory: `.`

4. Clique em "Deploy site"

5. O site estará disponível em um subdomínio do Netlify, que você pode personalizar nas configurações.

## Uso do Sistema de Atualização Manual

O script `atualizar_repositorio.py` permite adicionar novos documentos ao repositório e atualizar a interface web automaticamente.

### Instalação do Script de Atualização

1. Certifique-se de que o Python 3.6+ está instalado no servidor:
   ```bash
   python3 --version
   ```

2. Torne o script executável:
   ```bash
   chmod +x atualizar_repositorio.py
   ```

### Uso do Script

1. Execute o script:
   ```bash
   ./atualizar_repositorio.py
   ```

2. No menu principal, você terá as seguintes opções:
   - **Adicionar novo documento**: Permite adicionar um novo decreto, resolução ou portaria ao repositório
   - **Atualizar interface web**: Atualiza o arquivo index.html com os novos documentos adicionados
   - **Sair**: Encerra o script

### Adicionando um Novo Documento

1. Selecione a opção "Adicionar novo documento"
2. Escolha o tipo de documento (Decreto, Resolução ou Portaria)
3. Digite o título do documento
4. Informe a data de publicação no formato DD/MM/AAAA
5. Digite o conteúdo do documento (digite "FIM" em uma linha separada para terminar)
6. O documento será salvo no diretório correspondente ao ano e mês da data de publicação

### Atualizando a Interface Web

1. Após adicionar novos documentos, selecione a opção "Atualizar interface web"
2. O script atualizará automaticamente o arquivo index.html com os novos documentos
3. Faça upload do arquivo index.html atualizado para o servidor web

## Configuração para Acesso pelo ChatGPT

Para garantir que o ChatGPT possa acessar o conteúdo do repositório:

1. Certifique-se de que o site está acessível publicamente através de uma URL
2. Forneça a URL base do repositório ao configurar seu GPT personalizado
3. Certifique-se de que os arquivos de texto estão em formato acessível e sem bloqueios

## Manutenção e Atualização

Para manter o repositório atualizado:

1. Monitore regularmente o Diário Oficial de SP para novas publicações relacionadas à Polícia Penal
2. Use o script de atualização para adicionar novos documentos
3. Atualize a interface web após adicionar novos documentos
4. Faça backup regular dos arquivos do repositório

## Solução de Problemas

### Problemas Comuns

1. **Documentos não aparecem na interface web**:
   - Verifique se o script de atualização foi executado após adicionar os documentos
   - Verifique se o arquivo index.html foi atualizado e enviado para o servidor

2. **Erro ao executar o script de atualização**:
   - Verifique se o Python 3.6+ está instalado
   - Verifique se o script tem permissão de execução
   - Verifique se o diretório `site` existe no mesmo nível do script

3. **ChatGPT não consegue acessar o conteúdo**:
   - Verifique se o site está acessível publicamente
   - Verifique se não há bloqueios de acesso no servidor
   - Certifique-se de que os arquivos de texto estão em formato UTF-8

## Suporte

Para suporte adicional ou dúvidas sobre a instalação e uso do repositório, entre em contato com o administrador do sistema.
