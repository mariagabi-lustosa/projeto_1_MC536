### projeto_MC536
## Grupo ID 2

### Membros:  
&nbsp;&nbsp;&nbsp;Maria Gabriela Lustosa - RA:83183901  
&nbsp;&nbsp;&nbsp;Gabriel Cabra; - RA:83183901  
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

Nosso projeto para a disciplica MC536 - Banco de Dados visa estabelecer uma ligação entre os dados de conluintes do ensino superior no Brasil em determinada área do conhecimento, e os dados referentes as ofertas de emprego para essas áreas, analisando os dados com base em UF, Município e ano e mais.

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

**DataBase**:PostgreSQL  

**Linguagem**: Python  

**Bibliotecas**: panda, psycopg2  


## Organização do Projeto

<pre> 📁 meu-repo/ ├── README.md ├── datasets/ │ ├── indicadores_educacao.csv │ ├── rais_tabela4_2021.csv │ ├── rais_tabela4_2023.csv │ ├── rais_tabela4_joined.csv │ ├── rais_tabela6_2021.csv │ ├── rais_tabela6_2023.csv │ └── rais_tabela6_joined.csv ├── models/ │ ├── conpectual_models.png │ ├── physical_model.sql │ └── relational_model.png ├── preprocessed_dataset/ │ ├── RAIS_ano_base_2021_TABELA4.csv │ ├── RAIS_ano_base_2021_TABELA6.csv │ ├── RAIS_ano_base_2023_TABELA4.csv │ ├── RAIS_ano_base_2023_TABELA6.csv │ └── indicadores_trajetoria_educacao_superior_2019_2023.csv ├── projeto1/ │ └── arquivos/ │ ├── create_database.py │ ├── fill_database.py │ └── process_datasets.py ├── querries/ ├── main.py </pre>

## Data Processing


## Queries

**número de ingressantes em uma área em relação a média salarial na mesma, para um ano fixo**







