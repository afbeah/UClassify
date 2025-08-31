# UClassify: Análise e Classificação de E-mails com IA

O *UClassify* é uma aplicação web que utiliza inteligência artificial para classificar o conteúdo de e-mails e sugerir respostas automáticas. Com ele, você pode otimizar a triagem de mensagens, separando e-mails "Produtivos" de "Improdutivos" para uma gestão mais eficiente da sua caixa de entrada.

A aplicação aceita texto direto ou arquivos de texto (.txt) e PDF (.pdf), oferecendo uma solução prática e inteligente para automatizar tarefas de comunicação.

## Tecnologias e Funcionalidades

### Tecnologias Usadas

* Python: Linguagem de programação principal.

* Flask: Micro-framework web para a criação da aplicação.

* Hugging Face transformers: Biblioteca para utilizar modelos de IA pré-treinados para classificação de texto e geração de linguagem.

* PyPDF2: Biblioteca para a leitura e processamento de arquivos PDF.

* HTML, CSS e JavaScript: Utilizados no front-end para a interface do usuário.

* Vercel: Plataforma de deploy para hospedar a aplicação.

### Funcionalidades

* Classificação de E-mail: Analisa o sentimento do texto para classificá-lo como "Produtivo" ou "Improdutivo".

* Leitura de Arquivos: Aceita tanto texto colado quanto o upload de arquivos .txt e .pdf.

* Sugestão de Resposta: Gera respostas automáticas e contextuais com base na classificação do e-mail.

* Interface Simples e Intuitiva: O design foca na experiência do usuário, tornando a análise rápida e fácil.

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e rodar o UClassify em sua máquina.

1. Pré-requisitos
Certifique-se de ter o Python instalado. O projeto utiliza as dependências listadas no arquivo `requirements.txt.`

2. Instalação das Dependências
Navegue até o diretório raiz do projeto e instale as bibliotecas necessárias usando o pip:

`pip install -r requirements.txt`

3. Execução
Após a instalação, você pode iniciar o servidor web do Flask:

`python app.py`

O servidor será iniciado e você poderá acessar a aplicação em seu navegador no endereço: http://localhost:5000.

## Contribuições
Sinta-se à vontade para contribuir! Sugestões de melhorias, relatórios de bugs ou novas funcionalidades são sempre bem-vindos.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.