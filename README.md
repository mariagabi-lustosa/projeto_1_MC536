### projeto_MC536
## Grupo ID 2

### Membros:  
&nbsp;&nbsp;&nbsp;Maria Gabriela Lustosa Oliveira - RA: 188504  
&nbsp;&nbsp;&nbsp;Gabriel Cabral Romero Oliveira - RA: 247700  
&nbsp;&nbsp;&nbsp;Flavia Juliana Ventilari dos Santos - RA: 260438     


### Glossário

- [Descrição do Projeto](#descrica-do-projeto)
- [Esquema dos Databases](#esquema-dos-databases)
- [Datasets](#datasets)
- [Tecnologias Ultilizadas](#linguagens-ultilizadas)
- [Organização do Projeto](#Organização-do-projeto)
- [Data Processing](#data-processing)
- [Queries](#queries)


### Descrição do Projeto

Nosso projeto para a disciplica MC536 - Banco de Dados, orquestrada na Unicamp, que visa estabelecer uma ligação entre os dados de conluintes do ensino superior no Brasil em determinada área do conhecimento, e os dados referentes as ofertas de emprego para essas áreas, analisando os dados com base em UF, Município e ano e mais.

Essa análise nos chamou atenção entre as ODS da ONU, para percebemos como alunos da graduação vizualizam o mercado de trabalho, e como mudanças em áreas do mercado impactam na entrada e formação em cursos da graduação que estão envolvidos com essas áreas.

### Esquema dos Databases

![Preview do Modelo Conceitual](models/conceptual_model.png)
![Preview do Modelo Relacional](models/relational_model.png)
## [Modelo Físico:](models/physical_model.sql)

### DataSets

![Indicadores de Educação](datasets/indicadores_educacao.csv)

Dataset do INEP que nos mostra variados dados, incluindo ano de ingresso e de conlusão de alunos no ensino superior, o curso que estão matriculados, a instituição, UF e muito mais.
Link de acesso: [INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior/resultados)


--------------------------------------------------------------------------------------------------------------------------------------


![rais_tabela4_2021](datasets/rais_tabela4_2021.csv)
![rais_tabela6_2021](datasets/rais_tabela6_2021.csv)

Dataset do RAIS (Relação Anual de Informações Sociais) que nos mostra variados dados, incluindo ano , áreas de trabalho e suas médias salariais, UF, Município e muito mais, para dados 2020-2021.
Link de acesso: [RAIS_2021](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/RAIS)


![rais_tabela4_2023](datasets/rais_tabela4_2023.csv)
![rais_tabela6_2023](datasets/rais_tabela6_2023.csv)

Dataset do RAIS (Relação Anual de Informações Sociais) que nos mostra variados dados, incluindo ano , áreas de trabalho e suas médias salariais, UF, Município e muito mais, para dados 2022-2023.
Link de acesso: [RAIS_2023](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/RAIS)

A seguir estão os Datases conjuntos para os anos 2021-2023, das tabelas 4 e 6.

![rais_tabela4](datasets/rais_tabela4_joined.csv)
![rais_tabela6](datasets/rais_tabela4_joined.csv)



### Tecnologias Ultilizadas

**DataBase**: PostgreSQL  

**Linguagem**: Python 3.13

**Bibliotecas**: panda, psycopg2  


## Organização do Projeto

```
📦 PROJETO_MCS36
├── 📁 arquivos
│   ├── create_database.py
│   ├── fill_database.py
│   ├── process_datasets.py
│   └── run_queries.py
├── 📁 datasets
│   ├── indicadores_educacao.csv
│   ├── rais_tabela4_2021.csv
│   ├── rais_tabela4_2023.csv
│   ├── rais_tabela4_joined.csv
│   ├── rais_tabela6_2021.csv
│   ├── rais_tabela6_2023.csv
│   └── rais_tabela6_joined.csv
├── 📁 models
│   ├── conceptual_model.png
│   ├── physical_model.sql
│   └── relational_model.png
├── 📁 preprocessed_dataset
│   ├── indicadores_trajetoria_educacao_superior.csv
│   ├── RAIS_ano_base_2021_TABELA4.csv
│   ├── RAIS_ano_base_2021_TABELA6.csv
│   ├── RAIS_ano_base_2023_TABELA4.csv
│   └── RAIS_ano_base_2023_TABELA6.csv
├── 📁 projeto1
└── 📁 queries
    ├── query_1_result.csv
    ├── query_2_result.csv
    ├── query_3_result.csv
    ├── query_4_result.csv
    └── query_5_result.csv
```


## Data Processing


## Queries

![Query_1:](projeto_MC536/querries/query_1_result.csv) *20 municípios com mais emprego formal em setor específico (com filtro por ano)*  
![Query_2:](projeto_MC536/querries/query_2_result.csv) *Relação entre taxa de desistência e variação de remuneração por área em um determinado período de tempo",*  
![Query_3:](projeto_MC536/querries/query_3_result.csv) *Relação entre estados com queda na remuneração e taxa de desistência do curso*  
![Query_4:](projeto_MC536/querries/query_4_result.csv) *Relação entre estados com aumento de remuneração e taxa de desistência do curso*  
![Query_5:](projeto_MC536/querries/query_5_result.csv) *Partindo de um ano de referência, identifica quantos foram os ingressantes de uma determinada área em uma instituição específica*  





