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
- [Organização do Projeto](#Organização-do-projeto)
- [Executando o Projeto](#executando-o-projeto)
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



## Organização do Projeto

```
📦 PROJETO_MCS36
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
├── 📁 python_files
│   ├── create_database.py
│   ├── fill_database.py
│   ├── process_datasets.py
│   └── run_queries.py
└── 📁 queries
    ├── query_1_result.csv
    ├── query_2_result.csv
    ├── query_3_result.csv
    ├── query_4_result.csv
    └── query_5_result.csv
```


## Executando o Projeto

**Tecnologias Ultilizadas:**

**DataBase**: PostgreSQL  
**pgAdmin pode ser usado para faciliar a visualização do database.*

**Linguagem**: Python 3.13

**Bibliotecas do Python**: panda, psycopg2  

**Scripts:**

Execute `create_database.py`, depois `fill_database.py`, e então `run_queries.py`.  
O `process_dataset.py` é opcional caso deseje recriar os datasets.  
Execute os arquivos no terminal para poder ver o nosso projeto!



## Queries

![Query_1:](queries/query_1_result.csv) *Identifica os 20 municípios com mais empregos formais em um setor e ano específicos* 

![Query_2:](queries/query_2_result.csv) *Relação entre taxa de desistência média e variação de remuneração por área do conhecimento em um determinado período de tempo*  

![Query_3:](queries/query_3_result.csv) *Relação entre estados com queda na remuneração e taxa de desistência média dos cursos de graduação*  

![Query_4:](queries/query_4_result.csv) *Relação entre estados com aumento de remuneração e taxa de desistência média dos cursos de graduação*  

![Query_5:](queries/query_5_result.csv) *Partindo de um ano de referência, identifica quantos foram os ingressantes de uma determinada área em uma instituição específica*  





