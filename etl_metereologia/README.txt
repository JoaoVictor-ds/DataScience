## Monitoramento Meteorológico - Região dos Lagos
Este projeto é um pipeline de dados (ETL) automatizado que coleta previsões meteorológicas e alimenta um dashboard de monitoramento. O sistema extrai dados da API Open-Meteo, processa indicadores climáticos e os armazena em um banco de dados MySQL, onde a camada de visualização consome as informações via conexão direta.
## Funcionalidades

* Extração: Coleta de previsões para os próximos 7 dias via API Open-Meteo.
* Transformação: Cálculo de média diária de umidade a partir de dados horários, além de métricas de vento e temperatura.
* Carga: Persistência automatizada dos dados no MySQL.
* Visualização: Integração direta entre o banco de dados e o dashboard para atualização em tempo real.

## Tecnologias Utilizadas

* Linguagem: Python 3.x
* Bibliotecas: Pandas, SQLAlchemy, PyMySQL, Requests e Python-dotenv.
* Banco de Dados: MySQL.
* API: Open-Meteo (Weather Forecast).
* Automação: Agendador de Tarefas do Windows.

## Estrutura do Banco de Dados
O script alimenta a tabela previsao_clima com os seguintes campos principais:

* id_cidade: Identificador do município.
* data_previsao: Data da previsão meteorológica.
* id_condicao: Código de condição climática (WMO).
* temp_max / temp_min: Temperaturas extremas do dia.
* chuva_prob: Probabilidade máxima de precipitação.
* vento_vel / vento_dir: Intensidade e direção do vento.
* umidade_rel: Média calculada da umidade diária.
* data_coleta: Timestamp da execução do script.

## Configuração e Instalação

   1. Variáveis de Ambiente: Configure o arquivo .env na raiz do projeto:
   
   DB_HOST=seu_host
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=seu_nome_do_banco
   
   2. Instalação de Dependências:
   
   pip install requests pandas sqlalchemy pymysql python-dotenv
   
   3. Execução Manual:
   
   python main.py
   
   
## Automação e Dashboard

* Agendamento: O script é executado automaticamente via Agendador de Tarefas do Windows, garantindo que a base de dados seja atualizada sem intervenção manual.
* Conexão do Dashboard: A ferramenta de visualização está conectada diretamente ao MySQL, refletindo os novos dados assim que a carga é concluída.

## Cidades Monitoradas
O monitoramento cobre os municípios de: Araruama, Cabo Frio, Arraial do Cabo, Armação dos Búzios, São Pedro da Aldeia, Iguaba Grande, Saquarema e Rio das Ostras.
